import pikepdf
import os
import re


def split_pdf_by_bookmarks(input_pdf, output_dir):
    """
    Split a PDF file into separate files based on bookmarks/outline.
    
    Args:
        input_pdf (str): Path to the input PDF file
        output_dir (str): Directory where split PDFs will be saved
    """
    try:
        pdf = pikepdf.open(input_pdf)
        os.makedirs(output_dir, exist_ok=True)

        # Check if PDF has an outline
        try:
            outline = pdf.open_outline()
            if not outline.root:
                print("❌ No bookmarks found in the PDF")
                return
        except Exception as e:
            print(f"❌ Error accessing bookmarks: {e}")
            return

        # Get top-level bookmarks
        bookmarks = list(outline.root)

        if not bookmarks:
            print("❌ No top-level bookmarks found")
            return

        print(f"📚 Found {len(bookmarks)} bookmarks")

        for i, item in enumerate(bookmarks):
            try:
                # Clean up title for filename (remove/replace problematic characters)
                title = sanitize_filename(item.title)
                
                # Get the page number (pikepdf uses 0-based indexing)
                start_page_num = get_page_number_from_outline_item(pdf, item)
                
                if start_page_num is None:
                    print(f"⚠️ Skipping bookmark '{item.title}' - could not determine page number")
                    continue

                # Determine end page
                if i < len(bookmarks) - 1:
                    end_page_num = get_page_number_from_outline_item(pdf, bookmarks[i + 1])
                    if end_page_num is None:
                        end_page_num = len(pdf.pages)
                else:
                    end_page_num = len(pdf.pages)

                # Ensure we have valid page ranges
                if start_page_num >= end_page_num:
                    print(f"⚠️ Skipping bookmark '{item.title}' - invalid page range")
                    continue

                # Create new PDF with pages from start_page to end_page-1
                new_pdf = pikepdf.Pdf.new()
                for page_idx in range(start_page_num, end_page_num):
                    if page_idx < len(pdf.pages):
                        new_pdf.pages.append(pdf.pages[page_idx])

                # Save the new PDF
                output_file = os.path.join(output_dir, f"{i+1:02d}_{title}.pdf")
                new_pdf.save(output_file)
                new_pdf.close()
                
                page_count = end_page_num - start_page_num
                print(f"✅ Saved: {output_file} (pages {start_page_num+1}-{end_page_num}, {page_count} pages)")

            except Exception as e:
                print(f"❌ Error processing bookmark '{item.title}': {e}")
                continue

    except Exception as e:
        print(f"❌ Error opening PDF: {e}")
    finally:
        if 'pdf' in locals():
            pdf.close()


def sanitize_filename(title):
    """
    Clean up bookmark title to make it suitable for filename.
    
    Args:
        title (str): Original bookmark title
        
    Returns:
        str: Sanitized filename
    """
    if not title:
        return "untitled"
    
    # Replace problematic characters
    title = re.sub(r'[<>:"/\\|?*]', '_', title)  # Windows forbidden chars
    title = re.sub(r'\s+', '_', title)  # Replace whitespace with underscore
    title = title.strip('._')  # Remove leading/trailing dots and underscores
    
    # Limit length and ensure it's not empty
    title = title[:100] if len(title) > 100 else title
    return title if title else "untitled"


def get_page_number_from_outline_item(pdf, outline_item):
    """
    Get the 0-based page index from an OutlineItem.
    
    Args:
        pdf: pikepdf.Pdf object
        outline_item: OutlineItem from bookmark
        
    Returns:
        int or None: 0-based page index, or None if not found
    """
    try:
        # OutlineItem has a destination attribute
        if hasattr(outline_item, 'destination') and outline_item.destination:
            destination = outline_item.destination
            
            # Destination is a pikepdf.Array like [page_ref, /XYZ, left, top, zoom]
            if hasattr(destination, '__len__') and len(destination) > 0:
                page_ref = destination[0]  # First element is the page reference
                
                # The page reference looks like <Pdf.pages.from_objgen(35,0)>
                # We need to find which page in pdf.pages matches this reference
                return get_page_number_from_reference(pdf, page_ref)
        
        # Fallback: try using the action if destination doesn't work
        if hasattr(outline_item, 'action') and outline_item.action:
            action = outline_item.action
            if hasattr(action, 'D') and action.D:
                if hasattr(action.D, '__len__') and len(action.D) > 0:
                    page_ref = action.D[0]
                    return get_page_number_from_reference(pdf, page_ref)
        
        return None
        
    except Exception as e:
        print(f"⚠️ Error getting page number from outline item '{outline_item.title}': {e}")
        return None


def get_page_number_from_reference(pdf, page_ref):
    """
    Get the 0-based page index for a page reference from a bookmark.
    
    Args:
        pdf: pikepdf.Pdf object
        page_ref: Page reference object from bookmark destination
        
    Returns:
        int or None: 0-based page index, or None if not found
    """
    try:
        # The page reference appears to be something like <Pdf.pages.from_objgen(35,0)>
        # We need to find which page in pdf.pages has the same object generation number
        
        # Try to get the object generation info from the page reference
        if hasattr(page_ref, 'objgen'):
            target_objgen = page_ref.objgen
            
            # Search through all pages to find the one with matching objgen
            for i, page in enumerate(pdf.pages):
                if hasattr(page, 'objgen') and page.objgen == target_objgen:
                    return i
        
        # Alternative approach: try direct comparison
        for i, page in enumerate(pdf.pages):
            if page == page_ref:
                return i
            # Also try comparing the underlying objects
            if hasattr(page, 'obj') and hasattr(page_ref, 'obj'):
                if page.obj == page_ref.obj:
                    return i
        
        # Another approach: try using str representation to extract objgen numbers
        page_ref_str = str(page_ref)
        if 'from_objgen(' in page_ref_str:
            # Extract objgen numbers from string like "<Pdf.pages.from_objgen(35,0)>"
            import re
            match = re.search(r'from_objgen\((\d+),(\d+)\)', page_ref_str)
            if match:
                obj_num, gen_num = int(match.group(1)), int(match.group(2))
                target_objgen = (obj_num, gen_num)
                
                for i, page in enumerate(pdf.pages):
                    if hasattr(page, 'objgen') and page.objgen == target_objgen:
                        return i
        
        return None
        
    except Exception as e:
        print(f"⚠️ Error resolving page reference {page_ref}: {e}")
        return None


def get_page_number(pdf, page_ref):
    """
    Get the 0-based page index for a page reference.
    
    Args:
        pdf: pikepdf.Pdf object
        page_ref: Page reference from bookmark
        
    Returns:
        int or None: 0-based page index, or None if not found
    """
    # This function is now just a wrapper for the new implementation
    return get_page_number_from_reference(pdf, page_ref)


if __name__ == "__main__":
    input_pdf = r"C:\Users\IgorB\Downloads\AI Engineering by Chip Huyen.pdf"
    output_dir = r"C:\Users\IgorB\OneDrive\Documents\Dev\python-coding-hub\Python_Scripts\PDFs\output_dir"
    
    print(f"📄 Input PDF: {input_pdf}")
    print(f"📁 Output directory: {output_dir}")
    print("-" * 50)
    
    split_pdf_by_bookmarks(input_pdf, output_dir)