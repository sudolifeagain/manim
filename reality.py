from manim import *

class RealityAnimation(Scene):
    def construct(self):
        ## ==== 上段：Anagramのアニメーション ====
        src_text = "Let’s catch the frailty"
        target_chars = list("reality")  # '4'は src にないので除外

        def apply_first_match_color(text, match_chars, color="red"):
            result = ""
            used_chars = set()
            for c in text:
                if c in match_chars and c not in used_chars:
                    result += f"<span foreground='{color}'>{c}</span>"
                    used_chars.add(c)
                else:
                    result += c
            return result

        src_markup = apply_first_match_color(src_text, target_chars)
        tar_markup = "<span foreground='red'>reality</span> has left the chat"

        src = MarkupText(src_markup).move_to(ORIGIN)  # 中央に移動
        tar = MarkupText(tar_markup).move_to(ORIGIN)  # 中央に移動

        self.play(Write(src))
        self.wait(0.5)
        self.play(TransformMatchingShapes(src, tar, path_arc=PI / 2))
        self.wait(0.5)
