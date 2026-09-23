from generatecontent import copy_from_source_to_destination, generate_pages_recursive
import sys

def main():
    target_dir = "." if len(sys.argv) < 2 else sys.argv[1]
    base_url_path = "/" if len(sys.argv) < 3 else sys.argv[2]
    copy_from_source_to_destination(f"{target_dir}/static", f"{target_dir}/docs")
    generate_pages_recursive(f"{target_dir}/content", "./template.html", f"{target_dir}/docs", base_url_path)

if __name__ == "__main__":
    main()