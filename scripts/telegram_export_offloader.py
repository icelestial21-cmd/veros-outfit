import os
import shutil
import time
import sys

src_base = r"C:\Users\User\Downloads\Telegram Desktop\ChatExport_2026-09-26"
dst_base = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"

def is_file_closed(filepath):
    try:
        with open(filepath, 'r+b') as f:
            pass
        return True
    except (PermissionError, OSError):
        return False

def sync_pass():
    if not os.path.exists(src_base):
        return 0, 0

    os.makedirs(dst_base, exist_ok=True)
    
    total_bytes_moved = 0
    files_moved_count = 0

    # 1. Sync support folders (copy only, preserve structure)
    for folder in ['css', 'js', 'images']:
        src_f = os.path.join(src_base, folder)
        dst_f = os.path.join(dst_base, folder)
        if os.path.exists(src_f):
            os.makedirs(dst_f, exist_ok=True)
            for item in os.listdir(src_f):
                s_item = os.path.join(src_f, item)
                d_item = os.path.join(dst_f, item)
                if os.path.isfile(s_item) and (not os.path.exists(d_item) or os.path.getmtime(s_item) > os.path.getmtime(d_item)):
                    try:
                        shutil.copy2(s_item, d_item)
                    except Exception:
                        pass

    # 2. Sync html files (copy only, preserve source so Telegram can append)
    try:
        for item in os.listdir(src_base):
            if item.endswith('.html'):
                s_html = os.path.join(src_base, item)
                d_html = os.path.join(dst_base, item)
                if not os.path.exists(d_html) or os.path.getmtime(s_html) > os.path.getmtime(d_html):
                    shutil.copy2(s_html, d_html)
    except Exception:
        pass

    # 3. Offload heavy media (photos, video_files) -> Move to D: and delete from C:
    for media_folder in ['photos', 'video_files']:
        src_mf = os.path.join(src_base, media_folder)
        dst_mf = os.path.join(dst_base, media_folder)
        if not os.path.exists(src_mf):
            continue
        os.makedirs(dst_mf, exist_ok=True)

        try:
            entries = os.listdir(src_mf)
        except Exception:
            continue

        for filename in entries:
            s_file = os.path.join(src_mf, filename)
            d_file = os.path.join(dst_mf, filename)

            if not os.path.isfile(s_file):
                continue

            # If file already exists on D and has same size, we can safely delete from C
            if os.path.exists(d_file) and os.path.getsize(d_file) == os.path.getsize(s_file):
                try:
                    f_size = os.path.getsize(s_file)
                    os.remove(s_file)
                    total_bytes_moved += f_size
                    files_moved_count += 1
                except Exception:
                    pass
                continue

            # Otherwise, check if closed before moving
            if is_file_closed(s_file):
                try:
                    f_size = os.path.getsize(s_file)
                    shutil.copy2(s_file, d_file)
                    if os.path.getsize(d_file) == f_size:
                        os.remove(s_file)
                        total_bytes_moved += f_size
                        files_moved_count += 1
                except Exception:
                    pass

    return files_moved_count, total_bytes_moved

if __name__ == '__main__':
    continuous = '--loop' in sys.argv
    print(f"Starting Telegram Export Offloader Daemon to {dst_base}...")
    sys.stdout.flush()
    
    last_heartbeat = time.time()
    
    while True:
        count, b_moved = sync_pass()
        mb_moved = b_moved / (1024 * 1024)
        if count > 0:
            print(f"[{time.strftime('%X')}] Offloaded {count} files ({mb_moved:.2f} MB) to D: drive.")
            sys.stdout.flush()
            last_heartbeat = time.time()
        elif time.time() - last_heartbeat > 60:
            print(f"[{time.strftime('%X')}] Monitoring active. Telegram export queue clear.")
            sys.stdout.flush()
            last_heartbeat = time.time()
        
        if not continuous:
            break
            
        time.sleep(4)
