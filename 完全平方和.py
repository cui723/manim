from manim import *

class SquareFormulaProof(Scene):
    def construct(self):
        # 设置边长 a 和 b
        a = 2
        b = 1
        total = a + b

        # 创建正方形
        square = Square(side_length=total, color=WHITE)
        square.shift(LEFT * 3)
        self.play(Create(square))

        # 添加大括号标注 a + b（下方和左侧）
        # 下方括号
        bottom_brace = BraceBetweenPoints(
            square.get_corner(DL),
            square.get_corner(DR),
            direction=DOWN,
            color=WHITE
        )
        bottom_brace.stretch_to_fit_height(0.1)  # 更细
        bottom_label = bottom_brace.get_tex(r"a + b", buff=0.2).set_color(WHITE)

        # 左侧括号
        left_brace = BraceBetweenPoints(
            square.get_corner(DL),
            square.get_corner(UL),
            direction=LEFT,
            color=WHITE
        )
        left_brace.stretch_to_fit_width(0.1)  # 更细
        left_label = left_brace.get_tex(r"a + b", buff=0.2).set_color(WHITE)

        self.play(GrowFromCenter(bottom_brace), FadeIn(bottom_label))
        self.play(GrowFromCenter(left_brace), FadeIn(left_label))


        # 获取边缘位置
        left = square.get_left()
        bottom = square.get_bottom()
        top = square.get_top()
        right = square.get_right()

        # 虚线划分（用于 a=2, b=1）
        a_pos_x = left[0] + a
        a_pos_y = bottom[1] + a

        v_line = DashedLine(start=[a_pos_x, bottom[1], 0], end=[a_pos_x, top[1], 0])
        h_line = DashedLine(start=[left[0], a_pos_y, 0], end=[right[0], a_pos_y, 0])
        self.play(Create(v_line), Create(h_line))

        # 边长标注
        # "a" 的标注：在左下角的 a×a 区域的虚线旁
        a_label_left = MathTex("a").next_to(v_line, LEFT, buff=0.1).shift(DOWN * 0.5)  # 水平向左移
        a_label_bottom = MathTex("a").next_to(h_line, DOWN, buff=0.1).shift(LEFT * 0.5)  # 竖直向下移

        # "b" 的标注：在右上角的 b×b 区域的虚线旁
        b_label_right = MathTex("b").next_to(v_line, RIGHT, buff=0.4).shift(UP * 0.25)
        b_label_top = MathTex("b").next_to(h_line, UP, buff=0.3).shift(RIGHT * 0.35)

        length_labels = VGroup(a_label_left, a_label_bottom, b_label_right, b_label_top)
        self.play(Write(length_labels))

        # 着色区域前，先定义 origin
        origin = square.get_corner(DL)

        def colored_rect(x, y, w, h, color):
            return Rectangle(width=w, height=h, fill_color=color, fill_opacity=0.5, stroke_width=0) \
                .move_to(origin + RIGHT * (x + w / 2) + UP * (y + h / 2))

        def region_center(x_min, x_max, y_min, y_max):
            return [(x_min + x_max) / 2 + origin[0], (y_min + y_max) / 2 + origin[1], 0]

        # 依次显示区域标注 + 上色
        area_steps = [
            ("a^2", BLUE, colored_rect(0, 0, a, a, BLUE), region_center(0, a, 0, a)),
            ("ab", GREEN, colored_rect(a, 0, b, a, GREEN), region_center(a, a + b, 0, a)),
            ("ab", GREEN, colored_rect(0, a, a, b, GREEN), region_center(0, a, a, a + b)),
            ("b^2", RED, colored_rect(a, a, b, b, RED), region_center(a, a + b, a, a + b)),
        ]

        for tex, color, rect, pos in area_steps:
            label = MathTex(r"\boldsymbol{" + tex + r"}", color=color).move_to(pos)
            self.play(Write(label))
            self.play(FadeIn(rect))

        self.wait(1)

        # 展开公式（颜色对应区域，放在图形右边）
        formula1 = MathTex(
            r"(a + b)^2 = a^2 + ab + ab + b^2",
            tex_to_color_map={"a^2": BLUE, "ab": GREEN, "b^2": RED}
        ).scale(0.9).next_to(square, RIGHT, buff=1)

        formula2 = MathTex(
            r"(a + b)^2 = a^2 + 2ab + b^2",
            tex_to_color_map={"a^2": BLUE, "ab": GREEN, "b^2": RED}
        ).scale(1.1).next_to(square, RIGHT, buff=1)
        # 展开公式出现（右侧 + 上色 + 慢慢写）
        self.play(Write(formula1), run_time=3)
        self.wait(1)
        self.play(Transform(formula1, formula2), run_time=2.5)
        self.wait(2)
