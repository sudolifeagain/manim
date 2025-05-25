from manim import *

class RealityAnimation(Scene):
    def construct(self):
        # ==== 元のテキスト設定 ====
        src_text = "Let’s catch the frailty"
        target_chars = list("reality")

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

        # 元と変換後テキスト（中央表示）
        src_markup = apply_first_match_color(src_text, target_chars)
        tar_markup = "<span foreground='red'>reality</span> has left the chat"

        src = MarkupText(src_markup).move_to(ORIGIN)
        tar = MarkupText(tar_markup).move_to(ORIGIN)

        self.play(Write(src))
        self.wait(0.5)
        self.play(TransformMatchingShapes(src, tar, path_arc=PI / 2))
        self.wait(0.5)

        # ==== フェードアウト対象：has left the chat ====
        reality_text = tar[:7]  # "reality"
        suffix_text = tar[7:]   # " has left the chat"
        self.play(Uncreate(suffix_text))
        self.wait(0.3)

        # ==== "a" → "4" 差し替え ====
        # 新しい文字列 re4lity を構築
        re4lity = VGroup()
        letters = list("re4lity")
        colors = ["#FF0000", "#FF0000", "#3355FF", "#FF0000", "#FF0000", "#FF0000", "#FF0000"]

        for i, (char, color) in enumerate(zip(letters, colors)):
            t = Text(char, color=color)
            t.move_to(reality_text[i])  # 各文字を元の位置に
            re4lity.add(t)

        # reality を 1文字ずつ FadeTransform
        animations = [
            FadeTransform(reality_text[i], re4lity[i]) for i in range(7)
        ]
        self.play(*animations)
        self.wait(0.3)

        # ==== 最後に re4lity を中央に移動 ====
        self.play(re4lity.animate.scale(1.9).move_to(ORIGIN))
        self.wait()
