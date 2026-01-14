"""Standalone desktop GUI for HampterLiker using tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from typing import Optional
from queue import Queue, Empty
import logging
import webbrowser

from config import YouTubeConfig
from youtube_service import (
    get_authenticated_service,
    like_all_channel_videos,
    Video
)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Modern color palette
COLORS = {
    'primary': '#667eea',
    'primary_dark': '#5568d3',
    'secondary': '#764ba2',
    'accent': '#f093fb',
    'success': '#4ade80',
    'warning': '#fbbf24',
    'error': '#ef4444',
    'bg_dark': '#1e1b4b',
    'bg_light': '#f8fafc',
    'card_bg': '#ffffff',
    'text_dark': '#1e293b',
    'text_light': '#64748b',
    'border': '#e2e8f0',
}


class HampterLikerGUI:
    """Standalone desktop GUI for HampterLiker."""

    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("🐹 HampterLiker")
        self.root.geometry("700x850")
        self.root.resizable(False, False)

        # Set background with gradient effect (using solid color as base)
        self.root.configure(bg=COLORS['bg_light'])

        # State
        self.is_running = False
        self.message_queue: Queue = Queue()
        self.current_channel_url: Optional[str] = None

        # Create custom styles
        self._create_styles()

        # Create UI
        self._create_widgets()

        # Start message processor
        self._process_messages()

    def _create_styles(self) -> None:
        """Create custom ttk styles for modern look."""
        style = ttk.Style()

        # Configure progress bar style
        style.theme_use('clam')
        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor=COLORS['border'],
            bordercolor=COLORS['border'],
            background=COLORS['primary'],
            lightcolor=COLORS['primary'],
            darkcolor=COLORS['primary_dark'],
            thickness=8
        )

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=COLORS['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Header card with gradient-like effect
        header_card = tk.Frame(main_frame, bg=COLORS['primary'], relief=tk.FLAT)
        header_card.pack(fill=tk.X, pady=(0, 25))

        # Add subtle shadow effect with border
        header_inner = tk.Frame(header_card, bg=COLORS['primary'], padx=30, pady=35)
        header_inner.pack(fill=tk.BOTH)

        emoji_label = tk.Label(
            header_inner,
            text="🐹",
            font=("Arial", 80),
            bg=COLORS['primary']
        )
        emoji_label.pack()

        title_label = tk.Label(
            header_inner,
            text="HampterLiker",
            font=("Helvetica", 38, "bold"),
            bg=COLORS['primary'],
            fg="white"
        )
        title_label.pack(pady=(10, 5))

        subtitle_label = tk.Label(
            header_inner,
            text="Automatically like every video on a channel",
            font=("Helvetica", 13),
            bg=COLORS['primary'],
            fg="#e0e7ff"
        )
        subtitle_label.pack()

        # Channel card - modern card design
        channel_card = tk.Frame(main_frame, bg=COLORS['card_bg'], relief=tk.FLAT, bd=0)
        channel_card.pack(fill=tk.X, pady=(0, 20))

        channel_inner = tk.Frame(channel_card, bg=COLORS['card_bg'], padx=30, pady=25)
        channel_inner.pack(fill=tk.BOTH)

        input_label = tk.Label(
            channel_inner,
            text="TARGET CHANNEL",
            font=("Helvetica", 11, "bold"),
            bg=COLORS['card_bg'],
            fg=COLORS['text_light']
        )
        input_label.pack(anchor=tk.W, pady=(0, 12))

        # Channel display with modern styling
        channel_display_frame = tk.Frame(
            channel_inner,
            bg=COLORS['bg_light'],
            relief=tk.FLAT,
            bd=0
        )
        channel_display_frame.pack(fill=tk.X)

        channel_display = tk.Label(
            channel_display_frame,
            text="@the_hampter",
            font=("Helvetica", 20, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['primary'],
            padx=20,
            pady=15,
            anchor=tk.W
        )
        channel_display.pack(fill=tk.X)

        # Store the channel handle
        self.channel_handle = "@the_hampter"

        # Start button with modern styling
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_light'])
        button_frame.pack(fill=tk.X, pady=(0, 20))

        self.start_button = tk.Button(
            button_frame,
            text="🚀  Start Liking Videos",
            font=("Helvetica", 15, "bold"),
            bg=COLORS['secondary'],
            fg="white",
            activebackground=COLORS['primary_dark'],
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=18,
            cursor="hand2",
            command=self._on_start_clicked
        )
        self.start_button.pack(fill=tk.X)

        # Add hover effect binding
        self.start_button.bind("<Enter>", lambda e: self.start_button.config(bg=COLORS['primary_dark']))
        self.start_button.bind("<Leave>", lambda e: self.start_button.config(bg=COLORS['secondary']))

        # Progress card - modern card design
        progress_card = tk.Frame(main_frame, bg=COLORS['card_bg'], relief=tk.FLAT, bd=0)
        progress_card.pack(fill=tk.BOTH, expand=True)

        progress_inner = tk.Frame(progress_card, bg=COLORS['card_bg'], padx=30, pady=25)
        progress_inner.pack(fill=tk.BOTH, expand=True)

        # Status with modern styling
        status_header = tk.Label(
            progress_inner,
            text="STATUS",
            font=("Helvetica", 11, "bold"),
            bg=COLORS['card_bg'],
            fg=COLORS['text_light']
        )
        status_header.pack(anchor=tk.W, pady=(0, 8))

        self.status_label = tk.Label(
            progress_inner,
            text="Ready to start",
            font=("Helvetica", 13),
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        )
        self.status_label.pack(anchor=tk.W, pady=(0, 18))

        # Modern progress bar
        progress_container = tk.Frame(progress_inner, bg=COLORS['border'], height=10)
        progress_container.pack(fill=tk.X, pady=(0, 20))

        self.progress = ttk.Progressbar(
            progress_container,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate',
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress.pack(fill=tk.X)

        # Channel link button (initially hidden) - modern styling
        self.channel_link_button = tk.Button(
            progress_inner,
            text="🔗  Open Channel on YouTube",
            font=("Helvetica", 12, "bold"),
            bg=COLORS['primary'],
            fg="white",
            activebackground=COLORS['primary_dark'],
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self._open_channel_link
        )
        # Don't pack it yet - will show after channel is found

        # Add hover effect
        self.channel_link_button.bind("<Enter>", lambda e: self.channel_link_button.config(bg=COLORS['primary_dark']))
        self.channel_link_button.bind("<Leave>", lambda e: self.channel_link_button.config(bg=COLORS['primary']))

        # Stats section - modern cards
        stats_container = tk.Frame(progress_inner, bg=COLORS['card_bg'])
        stats_container.pack(fill=tk.X, pady=(0, 20))

        # Total videos stat card
        total_card = tk.Frame(stats_container, bg=COLORS['bg_light'], relief=tk.FLAT, bd=0)
        total_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        total_inner = tk.Frame(total_card, bg=COLORS['bg_light'], padx=20, pady=20)
        total_inner.pack(fill=tk.BOTH, expand=True)

        total_header = tk.Label(
            total_inner,
            text="TOTAL VIDEOS",
            font=("Helvetica", 10, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['text_light']
        )
        total_header.pack()

        self.total_label = tk.Label(
            total_inner,
            text="0",
            font=("Helvetica", 42, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['primary']
        )
        self.total_label.pack(pady=(8, 0))

        # Liked videos stat card
        liked_card = tk.Frame(stats_container, bg=COLORS['bg_light'], relief=tk.FLAT, bd=0)
        liked_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        liked_inner = tk.Frame(liked_card, bg=COLORS['bg_light'], padx=20, pady=20)
        liked_inner.pack(fill=tk.BOTH, expand=True)

        liked_header = tk.Label(
            liked_inner,
            text="VIDEOS LIKED",
            font=("Helvetica", 10, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['text_light']
        )
        liked_header.pack()

        self.liked_label = tk.Label(
            liked_inner,
            text="0",
            font=("Helvetica", 42, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['success']
        )
        self.liked_label.pack(pady=(8, 0))

        # Log area with modern styling
        log_label = tk.Label(
            progress_inner,
            text="ACTIVITY LOG",
            font=("Helvetica", 11, "bold"),
            bg=COLORS['card_bg'],
            fg=COLORS['text_light']
        )
        log_label.pack(anchor=tk.W, pady=(10, 10))

        log_container = tk.Frame(progress_inner, bg=COLORS['bg_light'], relief=tk.FLAT, bd=0)
        log_container.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(
            log_container,
            height=9,
            font=("Menlo", 10),
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark'],
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED,
            padx=15,
            pady=15
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Footer with modern styling
        footer = tk.Label(
            main_frame,
            text="Made with 💕 for the Hampter community",
            font=("Helvetica", 10),
            bg=COLORS['bg_light'],
            fg=COLORS['text_light']
        )
        footer.pack(pady=(20, 0))

    def _log(self, message: str) -> None:
        """
        Add message to log area.

        Args:
            message: Message to log
        """
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _update_status(self, status: str) -> None:
        """
        Update status label.

        Args:
            status: Status message
        """
        self.status_label.config(text=status)

    def _update_progress(self, current: int, total: int) -> None:
        """
        Update progress bar.

        Args:
            current: Current progress
            total: Total items
        """
        if total > 0:
            percentage = (current / total) * 100
            self.progress['value'] = percentage
        else:
            self.progress['value'] = 0

    def _open_channel_link(self) -> None:
        """Open the YouTube channel in browser."""
        if self.current_channel_url:
            webbrowser.open(self.current_channel_url)

    def _update_stats(self, total: int, liked: int) -> None:
        """
        Update statistics display.

        Args:
            total: Total videos
            liked: Liked videos
        """
        self.total_label.config(text=str(total))
        self.liked_label.config(text=str(liked))

    def _on_start_clicked(self) -> None:
        """Handle start button click."""
        if self.is_running:
            messagebox.showwarning(
                "Already Running",
                "A liking process is already in progress!"
            )
            return

        # Use the fixed channel handle
        channel = self.channel_handle

        # Disable button with modern text
        self.start_button.config(state=tk.DISABLED, text="⏳  Processing...", bg=COLORS['text_light'])
        self.is_running = True

        # Clear log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

        # Reset stats
        self._update_stats(0, 0)
        self._update_progress(0, 100)

        # Start worker thread
        thread = threading.Thread(
            target=self._run_workflow,
            args=(channel,),
            daemon=True
        )
        thread.start()

    def _run_workflow(self, channel: str) -> None:
        """
        Run the liking workflow in background thread.

        Args:
            channel: Channel handle
        """
        youtube_config = YouTubeConfig.default()

        try:
            # Authentication
            self.message_queue.put(("status", "🔐 Authenticating with YouTube..."))
            self.message_queue.put(("log", "Starting authentication..."))

            youtube = get_authenticated_service(youtube_config)

            self.message_queue.put(("log", "✅ Authentication successful!"))

            # Finding channel
            self.message_queue.put(("status", f"🔍 Finding channel: {channel}"))
            self.message_queue.put(("log", f"Searching for channel: {channel}"))

            # Progress callback
            def on_progress(current: int, total: int, video: Video) -> None:
                """Handle progress updates."""
                self.message_queue.put(("progress", (current, total)))
                self.message_queue.put(("stats", (total, current)))
                self.message_queue.put(("status", f"👍 Liking videos... {current}/{total}"))
                if current % 5 == 0:  # Log every 5 videos
                    self.message_queue.put(("log", f"Liked {current}/{total} videos..."))

            # Execute workflow
            channel_obj, videos, results = like_all_channel_videos(
                youtube,
                channel,
                on_progress
            )

            if not channel_obj:
                self.message_queue.put(("error", f"Channel not found: {channel}"))
                return

            # Create channel URL and show link button
            channel_url = f"https://www.youtube.com/{channel_obj.handle}"
            self.message_queue.put(("channel_link", channel_url))

            self.message_queue.put(("log", f"✅ Found channel: {channel_obj.handle}"))
            self.message_queue.put(("log", f"📺 Found {len(videos)} videos"))
            self.message_queue.put(("stats", (len(videos), 0)))

            # Wait for completion
            self.message_queue.put(("progress", (len(results), len(videos))))

            # Check if quota was exceeded
            quota_exceeded = any(r.quota_exceeded for r in results)
            successful = sum(1 for r in results if r.success)

            # Summary
            self.message_queue.put(("log", "=" * 40))
            if quota_exceeded:
                self.message_queue.put(("log", f"⚠️ Stopped: YouTube API quota exceeded"))
                self.message_queue.put(("log", f"Successfully liked {successful}/{len(videos)} videos"))
                self.message_queue.put(("log", f"Quota resets daily at midnight Pacific Time"))
                self.message_queue.put(("status", "⚠️ Quota Exceeded - Try again tomorrow!"))
                self.message_queue.put(("complete", None))

                messagebox.showwarning(
                    "Quota Exceeded ⚠️",
                    f"YouTube API quota exceeded!\n\n"
                    f"Successfully liked {successful}/{len(videos)} videos.\n\n"
                    f"💡 The quota resets daily at midnight Pacific Time.\n"
                    f"Try again tomorrow to like the remaining videos!"
                )
            else:
                self.message_queue.put(("log", f"✅ Completed!"))
                self.message_queue.put(("log", f"Successfully liked {successful}/{len(videos)} videos"))
                self.message_queue.put(("status", "✅ Completed! 🎉🐹🎊"))
                self.message_queue.put(("complete", None))

                messagebox.showinfo(
                    "Success! 🐹",
                    f"Successfully liked {successful}/{len(videos)} videos!\n\nHampter is happy! 🎉"
                )

        except Exception as e:
            logger.exception("Error in workflow")
            error_msg = f"Error: {str(e)}"
            self.message_queue.put(("error", error_msg))
            messagebox.showerror("Error", error_msg)

    def _process_messages(self) -> None:
        """Process messages from worker thread."""
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()

                if msg_type == "log":
                    self._log(data)
                elif msg_type == "status":
                    self._update_status(data)
                elif msg_type == "progress":
                    current, total = data
                    self._update_progress(current, total)
                elif msg_type == "stats":
                    total, liked = data
                    self._update_stats(total, liked)
                elif msg_type == "channel_link":
                    self.current_channel_url = data
                    self.channel_link_button.pack(fill=tk.X, pady=(0, 15))
                    self._log(f"🔗 Channel link: {data}")
                elif msg_type == "error":
                    self._log(f"❌ ERROR: {data}")
                    self._update_status("❌ Error occurred")
                    self.start_button.config(
                        state=tk.NORMAL,
                        text="🚀  Start Liking Videos",
                        bg=COLORS['secondary']
                    )
                    self.is_running = False
                elif msg_type == "complete":
                    self.start_button.config(
                        state=tk.NORMAL,
                        text="✅  Completed! Run Again?",
                        bg=COLORS['success']
                    )
                    self.is_running = False

        except Empty:
            pass

        # Schedule next check
        self.root.after(100, self._process_messages)


def main() -> None:
    """Main entry point."""
    root = tk.Tk()
    app = HampterLikerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
