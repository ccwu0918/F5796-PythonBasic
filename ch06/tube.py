import argparse
import os
import platform
from pytubefix import YouTube, exceptions
import subprocess
import re # 引入正規表示式模組

# 清除檔名中的不合法字元，避免存檔錯誤。
def check_filename(title):
    illegals = r'[\/\\:*\?"<>|]'  # 常見的不合法存檔名稱字元
    # 將找到的不合法字元替換成空字串
    renamed = re.sub(illegals, '', title).strip('. ')

    return renamed

def pyTube_folder():
    sys = platform.system()        # 取得作業系統名稱
    home = os.path.expanduser('~') # 取得使用者家目錄

    folder_map = {
        'Windows': os.path.join(home, 'Videos', 'PyTube'),
        'Darwin': os.path.join(home, 'Movies', 'PyTube')
    }
    folder = folder_map.get(sys, os.path.join(home, 'Videos', 'PyTube'))
    # .get() 的邏輯等同於底下這段 if/elif/else
    # if sys == 'Darwin':  # 若是macOS…
    #     folder = os.path.join(home, 'Movies', 'PyTube')
    # else:  # 其他作業系統（Windows和Linux）
    #     folder = os.path.join(home, 'Videos', 'PyTube')

    # os.makedirs(folder, exist_ok=True)
    return folder


def onProgress(stream, chunk, remains):
    if stream.filesize > 0:
        total = stream.filesize
        percent = (total - remains) / total * 100
        print('下載中… {:05.2f}%'.format(percent), end='\r')


def video_res(yt):
    res_set = set()
    streams = yt.streams.filter(adaptive=True)
    for s in streams:
        if s.resolution:
            res_set.add(s.resolution)

    if not res_set:
        streams = yt.streams.filter(progressive=True)
        for s in streams:
            if s.resolution:
                res_set.add(s.resolution)

    return sorted(list(res_set), reverse=True, key=lambda s: int(s[:-1]))


def download_video(yt, res, folder):
    video = yt.streams.filter(resolution=res, adaptive=True).first()
    if not video:
        print(f"錯誤：找不到 {res} 解析度的視訊。")
        return None
    print(f"\n開始下載視訊檔 ({res})...")
    return video.download(output_path=folder, filename_prefix="temp_video_")


def download_audio(yt, folder):
    # target = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    # if not target:
    #     print("錯誤：找不到可用的音訊流。")
    #     return None
    # print("\n開始下載聲音檔...")
    # return target.download(output_path=folder, filename_prefix="temp_audio_")
    print("正在尋找最高品質的聲音串流...")
    # audio = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    audio = yt.streams.get_audio_only()

    # 檢查是否找到聲音串流
    if audio:
        print('\n下載聲音檔…')
        return audio.download(output_path=folder, filename_prefix="audio_")
    else:
        print("\n找不到任何聲音檔。")
        return None


def merge_media(video_path, audio_path, output_path):
    print("正在合併視訊和聲音...")
    # cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c copy -y "{output_path}"'
    cmd_list = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-c', 'copy', '-y',
        output_path
    ]
    try:
        subprocess.run(cmd_list, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(video_path)
        os.remove(audio_path)
        print(f'視訊和聲音合併完成！檔案儲存於：{output_path}')
    except Exception as e:
        print(f'合併過程中發生錯誤: {e}')
        print("請確認 ffmpeg 已正確安裝並設定在系統環境變數中。")


def main():
    parser = argparse.ArgumentParser(description="下載 YouTube 影片並自動合併音訊。")
    parser.add_argument("url", help="指定YouTube視訊網址")
    parser.add_argument("-sd", action="store_true", help="選擇普通（480P）畫質")
    parser.add_argument("-hd", action="store_true", help="選擇HD（720P）畫質")
    parser.add_argument("-fhd", action="store_true", help="選擇Full HD（1080P）畫質")
    parser.add_argument("-a", action="store_true", help="僅下載聲音")

    args = parser.parse_args()
    download_folder = pyTube_folder()

    try:
        print("正在連線至 YouTube...")
        yt = YouTube(args.url, on_progress_callback=onProgress)
        
        # 在所有操作之前，先淨化檔名。
        safe_title = check_filename(yt.title)
        print(f"影片標題: {yt.title}")
        print(f"將使用的安全檔名: {safe_title}")

        if args.a:
            download_audio(yt, download_folder)
            return # 離開main()，結束程式。

        print("正在分析可用的影片格式...")
        res_list = video_res(yt)
        if not res_list:
            print("錯誤：此影片找不到任何可用的視訊檔。")
            return  # 離開main()，結束程式。

        # 選擇解析度
        target_res = None   # 下載目標解析度
        desired_res = None  # 使用者指定的解析度
        if args.fhd: desired_res = "1080p"
        elif args.hd: desired_res = "720p"
        elif args.sd: desired_res = "480p"

        # target_res = desired_res # 先假設影片有使用者指定的解析度
        if desired_res and desired_res in res_list:
            target_res = desired_res
        else:
            if desired_res: print(f'找不到您指定的解析度 {desired_res}，可用的解析度如下：')
            else: print('請選擇要下載的解析度：')
            for i, res in enumerate(res_list): print(f'{i+1}) {res}')
            val = input(f'請選擇（預設為 1: {res_list[0]}）：')
            try:
                choice_index = int(val) - 1
                target_res = res_list[choice_index] if 0 <= choice_index < len(res_list) else res_list[0]
            except ValueError:
                target_res = res_list[0]

        print(f"已確定下載解析度: {target_res}")
        output_filename = f"{safe_title} ({target_res}).mp4"
        full_filepath = os.path.join(download_folder, output_filename)

        # 檢查檔案是否已存在，避免重複下載
        if os.path.exists(full_filepath):
            print(f"檔案 '{full_filepath}' 已存在，略過下載。")
            return # 離開main()，結束程式。

        print("正在搜尋指定的影片串流...")
        video = yt.streams.filter(resolution=target_res, progressive=True).first()
        
        if video:
            print(f"\n找到包含聲音的合併檔 ({target_res})，開始下載...")
            # 檢查檔名是否包含不安全字元
            video.download(output_path=download_folder, filename=output_filename)
            print("\r下載完成！")
        else:
            print(f"\n未找到合併檔，將分別下載視訊 ({target_res}) 和聲音後合併。")
            
            video_path = download_video(yt, target_res, download_folder)
            if not video_path: return
            print("\r視訊檔下載完成！")

            audio_path = download_audio(yt, download_folder)
            if not audio_path:  # 若聲音檔下載失敗，則刪除已下載的視訊檔
                if os.path.exists(video_path): os.remove(video_path)
                return
            print("\r聲音檔下載完成！")
            # 合併視訊和聲音檔
            merge_media(video_path, audio_path, full_filepath)

    except exceptions.PytubeFixError as e:
        print(f"\nPytube 發生錯誤: {e}")
    except Exception as e:
        print(f"\n執行過程中發生未預期的錯誤: {e}")

if __name__ == '__main__':
    main()