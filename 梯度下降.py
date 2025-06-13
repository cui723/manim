from manim import *

# def dashed_line_with_arrow(start, end, dash_length=0.1, color=ORANGE, stroke_width=5, tip_length=0.3):
#     """
#     创建一条从 start 到 end 的虚线，并在末尾添加箭头
#     """
#     # 创建虚线
#     dashed_line = DashedLine(start, end, dash_length=dash_length, color=color)
#     # 用 Arrow 创建箭头，再提取其 tip 部分
#     arrow_tip = Arrow(start, end, stroke_width=stroke_width, tip_length=tip_length, color=color).get_tip()
#     # 返回包含虚线和箭头 tip 的 VGroup
#     return VGroup(dashed_line, arrow_tip)

class GradientDescentAnimation(Scene):
    def setup(self):
        # 设置背景为白色
        self.camera.background_color = WHITE

        # 定义目标函数和导数
        self.func = lambda x: x ** 2
        self.derivative = lambda x: 2 * x

        # 创建坐标轴（新版Axes配置），坐标轴颜色为黑色，粗细较细
        self.axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 50, 10],
            x_axis_config={
                "color": BLACK,
                "include_ticks": False,
                "stroke_width": 2
            },
            y_axis_config={
                "color": BLACK,
                "include_ticks": False,
                "stroke_width": 2
            },
            tips=True
        )

        # 绘制函数曲线，颜色灰色且稍加粗以与坐标轴区分
        self.graph = self.axes.plot(self.func, color=GRAY, stroke_width=4)
        self.add(self.axes, self.graph)

        # 初始点（x0=6）以及对应小球
        # self.x0 = 6.0
        self.x0 = 6.0
        self.dot = Dot(color=BLUE, radius=0.1, stroke_color=BLACK, stroke_width=2)
        self.dot.move_to(self.axes.c2p(self.x0, self.func(self.x0)))
        self.add(self.dot)

        # ##  学习率为1时才需要用的条件
        # 创建虚线，x = -10 处，结束于函数图像的 y 值
        dashed_line_left = DashedLine(self.axes.c2p(-6, 0), self.axes.c2p(-6, (-6) ** 2), dash_length=0.1, stroke_width=2)
        dashed_line_left.set_color(GRAY)

        # 创建虚线，x = 10 处，结束于函数图像的 y 值
        dashed_line_right = DashedLine(self.axes.c2p(6, 0), self.axes.c2p(6, (6) ** 2), dash_length=0.1, stroke_width=2)
        dashed_line_right.set_color(GRAY)

        # 在 x=-10 和 x=10 的下方添加数字
        label_left = Text("-1", color=BLACK, font_size=24).next_to(self.axes.c2p(-6, 0), DOWN)
        label_right = Text("1", color=BLACK, font_size=24).next_to(self.axes.c2p(6, 0), DOWN)

        self.add(dashed_line_left, dashed_line_right, label_left, label_right)

        # 添加函数公式标签（使用Tex类），颜色用黑色，与背景对比
        self.func_label = Tex(r"$f(x) = x^2$", color=BLACK).to_corner(UL, buff=0.5)
        self.deriv_label = Tex(r"$f'(x) = 2x$", color=BLACK).next_to(self.func_label, DOWN)
        self.add(self.func_label, self.deriv_label)

    def gradient_step(self, x, lr):
        """梯度下降迭代公式"""
        return x - lr * self.derivative(x)


class LearningRateTooSmall(GradientDescentAnimation):
    """学习率过小（η=0.02）"""

    def construct(self):
        self.setup()
        lr = 0.02
        x = self.x0
        iterations = 30

        # 添加学习率标签
        lr_label = Tex(rf"$\eta = {lr}$", color=RED_D).to_corner(UR, buff=0.5)
        self.add(lr_label)

        # 迭代过程：每次迭代前先复制当前位置的小球，移动后旧的小球依旧保留
        for _ in range(iterations):
            new_x = self.gradient_step(x, lr)
            # arrow = Arrow(
            #     start=self.axes.c2p(x, self.func(x)),
            #     end=self.axes.c2p(new_x, self.func(new_x)),
            #     color=ORANGE,
            #     buff=0.1,
            #     stroke_width=5,
            #     tip_length=0.3
            # )
            #
            # self.play(Create(arrow), run_time=0.2)

            # 保留当前位置的小球（复制一个）
            self.add(self.dot.copy())

            # 确保原始小球始终位于最前面
            self.bring_to_front(self.dot)

            self.play(
                self.dot.animate.move_to(self.axes.c2p(new_x, self.func(new_x))),
                run_time=0.5
            )

            x = new_x
            # self.remove(arrow)
        self.wait(0.5)


class LearningRateOptimal1(GradientDescentAnimation):
    """合适学习率（η=0.2）"""

    def construct(self):
        self.setup()
        lr = 0.2
        x = self.x0
        iterations = 10

        # 添加学习率标签
        lr_label = Tex(rf"$\eta = {lr}$", color=RED_E).to_corner(UR, buff=0.5)
        self.add(lr_label)

        # 迭代过程：每次迭代前先复制当前位置的小球，移动后旧的小球依旧保留
        for _ in range(iterations):
            new_x = self.gradient_step(x, lr)
            # arrow = Arrow(
            #     start=self.axes.c2p(x, self.func(x)),
            #     end=self.axes.c2p(new_x, self.func(new_x)),
            #     color=ORANGE,
            #     buff=0.1,
            #     stroke_width=3,
            #     tip_length=0.2
            # )
            #
            # self.play(Create(arrow), run_time=0.5)

            # 保留当前位置的小球（复制一个）
            self.add(self.dot.copy())

            # 确保原始小球始终位于最前面
            self.bring_to_front(self.dot)

            self.play(
                self.dot.animate.move_to(self.axes.c2p(new_x, self.func(new_x))),
                run_time=0.5
            )
            x = new_x
            # self.remove(arrow)
        self.wait(0.5)


class LearningRateTooLarge(GradientDescentAnimation):
    """学习率过大（η=1.05），并调整坐标系范围以及显示黄色虚线轨迹"""

    def construct(self):
        # 设置背景为白色
        self.camera.background_color = WHITE

        # 重新创建坐标轴，设定更大的范围，以便展示迭代轨迹
        self.axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 50, 10],
            x_axis_config={
                "color": BLACK,
                "include_ticks": False,
                "stroke_width": 2
            },
            y_axis_config={
                "color": BLACK,
                "include_ticks": False,
                "stroke_width": 2
            },
            tips=True
        )
        self.graph = self.axes.plot(self.func, color=GRAY, stroke_width=4)
        self.clear()  # 清除旧对象
        self.add(self.axes, self.graph)

        # 重新添加公式标签
        self.func_label = Tex(r"$f(x) = x^2$", color=BLACK).to_corner(UL, buff=0.5)
        self.deriv_label = Tex(r"$f'(x) = 2x$", color=BLACK).next_to(self.func_label, DOWN)
        self.add(self.func_label, self.deriv_label)

        # 可根据需要调整初始点位置
        self.x0 = 4.0
        self.dot = Dot(color=BLUE, radius=0.1, stroke_color=BLACK, stroke_width=2)
        self.dot.move_to(self.axes.c2p(self.x0, self.func(self.x0)))
        self.add(self.dot)

        lr = 1.05
        iterations = 6

        lr_label = Tex(rf"$\eta = {lr}$", color=RED_E).to_corner(UR, buff=0.5)
        self.add(lr_label)

        # 用于保存所有迭代位置的点，便于绘制黄色虚线轨迹
        points = [self.dot.get_center()]

        for i in range(iterations):
            x = self.axes.p2c(self.dot.get_center())[0]  # 从当前小球位置反推出 x 坐标
            new_x = self.gradient_step(x, lr)

            # 保留当前位置的小球
            self.add(self.dot.copy())

            # 确保原始小球始终位于最前面
            self.bring_to_front(self.dot)

            self.play(
                self.dot.animate.move_to(self.axes.c2p(new_x, self.func(new_x))),
                run_time=1
            )

            # 记录新位置
            points.append(self.dot.get_center())

            # 绘制实线箭头
            if len(points) > 1:
                start, end = points[-2], points[-1]
                arrow = Arrow(
                    start, end,
                    color=ORANGE,
                    stroke_width=2,
                    # stroke_opacity = 0.5,
                    tip_length=0.25,
                    stroke_opacity=0.8 - (i * 0.1),
                    buff=0.1,   # 箭头紧贴小球位置
                )
                self.add(arrow)

            # # 每次迭代后，用黄色虚线连结所有位置
            # dashed_segments = VGroup()
            # for i in range(len(points) - 1):
            #     seg = DashedLine(points[i], points[i + 1], dash_length=0.1, color=ORANGE)
            #     dashed_segments.add(seg)
            # self.add(dashed_segments)

        self.wait(0.5)



    # def construct(self):
    #     # 设置背景为白色
    #     self.camera.background_color = WHITE
    #
    #     # 重新创建坐标轴，设定更大的范围，以便展示迭代轨迹
    #     self.axes = Axes(
    #         x_range=[-10, 10, 1],
    #         y_range=[-10, 50, 10],
    #         x_axis_config={
    #             "color": BLACK,
    #             "include_ticks": False,
    #             "stroke_width": 2
    #         },
    #         y_axis_config={
    #             "color": BLACK,
    #             "include_ticks": False,
    #             "stroke_width": 2
    #         },
    #         tips=True
    #     )
    #     self.graph = self.axes.plot(self.func, color=GRAY, stroke_width=4)
    #     self.clear()  # 清除旧对象
    #     self.add(self.axes, self.graph)
    #
    #     # 重新添加公式标签
    #     self.func_label = Tex(r"$f(x) = x^2$", color=BLACK).to_corner(UL, buff=0.5)
    #     self.deriv_label = Tex(r"$f'(x) = 2x$", color=BLACK).next_to(self.func_label, DOWN)
    #     self.add(self.func_label, self.deriv_label)
    #
    #     # 可根据需要调整初始点位置
    #     self.x0 = 4.0
    #     self.dot = Dot(color=BLUE, radius=0.1, stroke_color=BLACK, stroke_width=2)
    #     self.dot.move_to(self.axes.c2p(self.x0, self.func(self.x0)))
    #     self.add(self.dot)
    #
    #     lr = 1.05
    #     iterations = 6
    #
    #     lr_label = Tex(rf"$\eta = {lr}$", color=RED_E).to_corner(UR, buff=0.5)
    #     self.add(lr_label)
    #
    #     # 用于保存所有迭代位置的点，便于绘制黄色虚线轨迹
    #     points = [self.dot.get_center()]
    #
    #     # 每次迭代后绘制虚线轨迹（带箭头）
    #     for _ in range(iterations):
    #         # 从当前小球位置反推出 x 坐标
    #         x = self.axes.p2c(self.dot.get_center())[0]
    #         new_x = self.gradient_step(x, lr)
    #
    #         # 保留当前位置的小球
    #         self.add(self.dot.copy())
    #         # 确保原始小球始终位于最前面
    #         self.bring_to_front(self.dot)
    #
    #         self.play(
    #             self.dot.animate.move_to(self.axes.c2p(new_x, self.func(new_x))),
    #             run_time=1
    #         )
    #         points.append(self.dot.get_center())
    #
    #         # 每次迭代后，用带箭头的虚线连结所有位置
    #         dashed_segments = VGroup()
    #         for i in range(len(points) - 1):
    #             seg = dashed_line_with_arrow(points[i], points[i + 1])
    #             dashed_segments.add(seg)
    #         self.add(dashed_segments)
    #
    #     self.wait()


class LearningRateOne(GradientDescentAnimation):
    """学习率为1.0的动画，同时满足背景、坐标轴及保留迭代位置的小球要求"""

    def construct(self):
        self.setup()
        lr = 1.0
        x = self.x0
        iterations = 6

        lr_label = Tex(rf"$\eta = {lr}$", color=RED_E).to_corner(UR, buff=0.5)
        self.add(lr_label)

        # 确保原始小球始终位于最前面
        self.bring_to_front(self.dot)

        for _ in range(iterations):
            new_x = self.gradient_step(x, lr)

            # 保留当前位置的小球
            self.add(self.dot.copy())

            # 确保原始小球始终位于最前面
            self.bring_to_front(self.dot)

            self.play(
                self.dot.animate.move_to(self.axes.c2p(new_x, self.func(new_x))),
                run_time=1
            )
            x = new_x
        self.wait(0.5)