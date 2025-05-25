from manim import *
import numpy as np

NEW_BLUE = "#68a8e1"

class Thumbnail(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configuration for axes
        self.y_max = 8
        self.y_min = 0
        self.x_max = 10
        self.x_min = -2
        self.y_axis_height = 5
        self.x_axis_width = 8
        
    def setup_axes(self, animate=True):
        """Setup coordinate axes"""
        self.axes = Axes(
            x_range=[self.x_min, self.x_max, 1],
            y_range=[self.y_min, self.y_max, 1],
            x_length=self.x_axis_width,
            y_length=self.y_axis_height,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=False
        )
        
        if animate:
            self.play(Create(self.axes))
        else:
            self.add(self.axes)
            
    def coords_to_point(self, x, y):
        """Convert coordinates to point in scene"""
        return self.axes.coords_to_point(x, y)
        
    def get_graph(self, func, x_min=None, x_max=None, **kwargs):
        """Get graph of function"""
        if x_min is None:
            x_min = self.x_min
        if x_max is None:
            x_max = self.x_max
            
        graph = self.axes.plot(func, x_range=[x_min, x_max], **kwargs)
        # Add the underlying function as an attribute for compatibility
        graph.underlying_function = func
        return graph
        
    def get_secant_slope_group(self, x, graph, dx, df_label=None, dx_label=None, 
                              dx_line_color=YELLOW, df_line_color=ORANGE, 
                              secant_line_color=RED):
        """Create secant line group"""
        func = graph.underlying_function
        
        # Points on the graph
        x1, x2 = x, x + dx
        y1, y2 = func(x1), func(x2)
        
        point1 = self.coords_to_point(x1, y1)
        point2 = self.coords_to_point(x2, y2)
        
        # Secant line (extended)
        secant_line = Line(
            self.coords_to_point(x1 - 0.5, y1 - 0.5 * (y2 - y1) / dx),
            self.coords_to_point(x2 + 0.5, y2 + 0.5 * (y2 - y1) / dx),
            color=secant_line_color
        )
        
        # dx line (horizontal)
        dx_line = Line(
            self.coords_to_point(x1, y1),
            self.coords_to_point(x2, y1),
            color=dx_line_color,
            stroke_width=4
        )
        
        # df line (vertical)
        df_line = Line(
            self.coords_to_point(x2, y1),
            self.coords_to_point(x2, y2),
            color=df_line_color,
            stroke_width=4
        )
        
        return VGroup(secant_line, dx_line, df_line)
        
    def get_riemann_rectangles(self, graph, dx=0.1, x_min=None, x_max=None, 
                              start_color=BLUE, end_color=GREEN, **kwargs):
        """Get Riemann rectangles"""
        if x_min is None:
            x_min = self.x_min
        if x_max is None:
            x_max = self.x_max
            
        func = graph.underlying_function
        rectangles = VGroup()
        
        x_values = np.arange(x_min, x_max, dx)
        n_rects = len(x_values)
        
        for i, x in enumerate(x_values):
            height = func(x)
            if height < 0:
                continue
                
            # Color interpolation
            alpha = i / max(1, n_rects - 1)
            color = interpolate_color(start_color, end_color, alpha)
            
            # Create rectangle
            rect = Rectangle(
                width=dx * self.axes.x_length / (self.x_max - self.x_min),
                height=height * self.axes.y_length / (self.y_max - self.y_min),
                color=color,
                **kwargs
            )
            
            # Position rectangle
            rect.move_to(self.coords_to_point(x + dx/2, height/2))
            rectangles.add(rect)
            
        return rectangles
        
    def get_riemann_rectangles_list(self, graph, n_iterations, start_color=BLUE, 
                                   end_color=GREEN, **kwargs):
        """Get list of Riemann rectangles with different subdivisions"""
        rectangles_list = []
        
        for i in range(1, n_iterations + 1):
            dx = (kwargs.get('x_max', self.x_max) - kwargs.get('x_min', self.x_min)) / (2**i)
            rects = self.get_riemann_rectangles(
                graph, dx=dx, start_color=start_color, end_color=end_color, **kwargs
            )
            rectangles_list.append(rects)
            
        return rectangles_list
        
    def transform_between_riemann_rects(self, start_rects, end_rects, 
                                       replace_mobject_with_target_in_scene=False, 
                                       **kwargs):
        """Transform between different Riemann rectangle sets"""
        if replace_mobject_with_target_in_scene:
            self.play(Transform(start_rects, end_rects), **kwargs)
            self.remove(start_rects)
            self.add(end_rects)
        else:
            self.play(Transform(start_rects, end_rects), **kwargs)

    def construct(self):
        self.show_function_graph()

    def show_function_graph(self):
        self.setup_axes(animate=False)
        
        # Define functions
        def func(x):
            return 0.1 * (x + 3 - 5) * (x - 3 - 5) * (x - 5) + 5

        def rect(x):
            return 2.775 * (x - 1.5) + 3.862
            
        # Create graphs
        recta = self.get_graph(rect, x_min=-1, x_max=5)
        graph = self.get_graph(func, x_min=0.2, x_max=9, color=NEW_BLUE)
        
        # Value trackers for points
        input_tracker_p1 = ValueTracker(1.5)
        input_tracker_p2 = ValueTracker(3.5)

        # Helper functions
        def get_x_value(input_tracker):
            return input_tracker.get_value()

        def get_y_value(input_tracker):
            return graph.underlying_function(get_x_value(input_tracker))

        def get_x_point(input_tracker):
            return self.coords_to_point(get_x_value(input_tracker), 0)

        def get_y_point(input_tracker):
            return self.coords_to_point(0, get_y_value(input_tracker))

        def get_graph_point(input_tracker):
            return self.coords_to_point(get_x_value(input_tracker), get_y_value(input_tracker))

        def get_v_line(input_tracker):
            return DashedLine(
                get_x_point(input_tracker), 
                get_graph_point(input_tracker), 
                stroke_width=2,
                color=WHITE
            )

        def get_h_line(input_tracker):
            return DashedLine(
                get_graph_point(input_tracker), 
                get_y_point(input_tracker), 
                stroke_width=2,
                color=WHITE
            )
        
        # Create triangles (arrows)
        input_triangle_p1 = Triangle(color=WHITE, fill_opacity=1)
        output_triangle_p1 = Triangle(color=WHITE, fill_opacity=1)
        input_triangle_p2 = Triangle(color=WHITE, fill_opacity=1)
        output_triangle_p2 = Triangle(color=WHITE, fill_opacity=1)
        
        for triangle in [input_triangle_p1, output_triangle_p1, 
                        input_triangle_p2, output_triangle_p2]:
            triangle.set_stroke(width=0)
            triangle.scale(0.1)
        
        # Rotate triangles to point in correct directions
        input_triangle_p1.rotate(PI)  # Point up
        input_triangle_p2.rotate(PI)  # Point up
        output_triangle_p1.rotate(-PI/2)  # Point right
        output_triangle_p2.rotate(-PI/2)  # Point right
        
        # Labels
        x_label_p1 = Text("a", color=WHITE, font_size=24)
        output_label_p1 = Text("f(a)", color=WHITE, font_size=24)
        x_label_p2 = Text("b", color=WHITE, font_size=24)
        output_label_p2 = Text("f(b)", color=WHITE, font_size=24)
        
        # Lines and dots
        v_line_p1 = get_v_line(input_tracker_p1)
        v_line_p2 = get_v_line(input_tracker_p2)
        h_line_p1 = get_h_line(input_tracker_p1)
        h_line_p2 = get_h_line(input_tracker_p2)
        graph_dot_p1 = Dot(color=WHITE)
        graph_dot_p2 = Dot(color=WHITE)

        # Position mobjects
        x_label_p1.next_to(v_line_p1, DOWN)
        x_label_p2.next_to(v_line_p2, DOWN)
        output_label_p1.next_to(h_line_p1, LEFT)
        output_label_p2.next_to(h_line_p2, LEFT)
        input_triangle_p1.next_to(v_line_p1, DOWN, buff=0)
        input_triangle_p2.next_to(v_line_p2, DOWN, buff=0)
        output_triangle_p1.next_to(h_line_p1, LEFT, buff=0)
        output_triangle_p2.next_to(h_line_p2, LEFT, buff=0)
        graph_dot_p1.move_to(get_graph_point(input_tracker_p1))
        graph_dot_p2.move_to(get_graph_point(input_tracker_p2))

        # Animation sequence
        self.play(Create(graph))
        
        # Add points and labels
        self.add(graph_dot_p1, graph_dot_p2)
        self.play(
            DrawBorderThenFill(input_triangle_p1),
            Write(x_label_p1),
            Create(v_line_p1),
            GrowFromCenter(graph_dot_p1),
            Create(h_line_p1),
            Write(output_label_p1),
            DrawBorderThenFill(output_triangle_p1),
            DrawBorderThenFill(input_triangle_p2),
            Write(x_label_p2),
            Create(v_line_p2),
            GrowFromCenter(graph_dot_p2),
            Create(h_line_p2),
            Write(output_label_p2),
            DrawBorderThenFill(output_triangle_p2),
            run_time=0.5
        )
        
        # Create secant slope group
        grupo_secante = self.get_secant_slope_group(
            1.5, graph, dx=2,
            df_label=None,
            dx_label=None,
            dx_line_color="#942357",
            df_line_color="#3f7d5c",
            secant_line_color=RED,
        )

        self.play(FadeIn(grupo_secante))

        # Riemann rectangles
        kwargs = {
            "x_min": 4,
            "x_max": 9,
            "fill_opacity": 0.75,
            "stroke_width": 0.25,
        }
        
        iteraciones = 6
        self.rect_list = self.get_riemann_rectangles_list(
            graph, iteraciones, start_color=PURPLE, end_color=ORANGE, **kwargs
        )
        
        # Create flat rectangles (height 0)
        flat_func = lambda x: 0
        flat_graph = self.get_graph(flat_func)
        flat_graph.underlying_function = flat_func
        
        flat_rects = self.get_riemann_rectangles(
            flat_graph, dx=0.5, 
            start_color=invert_color(PURPLE), 
            end_color=invert_color(ORANGE), 
            **kwargs
        )
        
        rects = self.rect_list[0]
        self.add(flat_rects)
        self.transform_between_riemann_rects(
            flat_rects, rects, 
            replace_mobject_with_target_in_scene=True,
            run_time=0.9
        )

        # Add "Manim" text
        picture = Group(*self.mobjects)
        picture.scale(0.6).to_edge(LEFT, buff=SMALL_BUFF)
        manim = Text("Manim", font_size=72).next_to(picture, RIGHT).shift(DOWN * 0.7)
        self.add(manim)
        
        self.wait(2)

# Simpler version without some complex features
class SimpleThumbnail(Scene):
    def construct(self):
        # Setup axes
        axes = Axes(
            x_range=[-2, 10, 1],
            y_range=[0, 8, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": WHITE}
        )
        
        # Define and plot function
        def func(x):
            return 0.1 * (x + 3 - 5) * (x - 3 - 5) * (x - 5) + 5
            
        graph = axes.plot(func, x_range=[0.2, 9], color=NEW_BLUE)
        
        # Add points
        x1, x2 = 1.5, 3.5
        y1, y2 = func(x1), func(x2)
        
        dot1 = Dot(axes.coords_to_point(x1, y1), color=WHITE)
        dot2 = Dot(axes.coords_to_point(x2, y2), color=WHITE)
        
        # Add vertical and horizontal lines
        v_line1 = DashedLine(
            axes.coords_to_point(x1, 0), 
            axes.coords_to_point(x1, y1), 
            color=WHITE
        )
        v_line2 = DashedLine(
            axes.coords_to_point(x2, 0), 
            axes.coords_to_point(x2, y2), 
            color=WHITE
        )
        h_line1 = DashedLine(
            axes.coords_to_point(0, y1), 
            axes.coords_to_point(x1, y1), 
            color=WHITE
        )
        h_line2 = DashedLine(
            axes.coords_to_point(0, y2), 
            axes.coords_to_point(x2, y2), 
            color=WHITE
        )
        
        # Labels
        label_a = Text("a", color=WHITE, font_size=24).next_to(v_line1, DOWN)
        label_b = Text("b", color=WHITE, font_size=24).next_to(v_line2, DOWN)
        label_fa = Text("f(a)", color=WHITE, font_size=24).next_to(h_line1, LEFT)
        label_fb = Text("f(b)", color=WHITE, font_size=24).next_to(h_line2, LEFT)
        
        # Secant line
        secant = Line(
            axes.coords_to_point(x1 - 0.5, y1 - 0.5 * (y2 - y1) / (x2 - x1)),
            axes.coords_to_point(x2 + 0.5, y2 + 0.5 * (y2 - y1) / (x2 - x1)),
            color=RED
        )
        
        # Riemann rectangles
        rectangles = VGroup()
        x_min, x_max = 4, 9
        n_rects = 20
        dx = (x_max - x_min) / n_rects
        
        for i in range(n_rects):
            x = x_min + i * dx
            height = func(x)
            
            rect = Rectangle(
                width=dx * axes.x_length / (axes.x_range[1] - axes.x_range[0]),
                height=height * axes.y_length / (axes.y_range[1] - axes.y_range[0]),
                fill_opacity=0.7,
                stroke_width=0.5
            )
            
            # Color gradient
            alpha = i / (n_rects - 1)
            rect.set_color(interpolate_color(PURPLE, ORANGE, alpha))
            rect.move_to(axes.coords_to_point(x + dx/2, height/2))
            rectangles.add(rect)
        
        # Animation
        self.add(axes)
        self.play(Create(graph))
        self.play(
            Create(v_line1), Create(v_line2),
            Create(h_line1), Create(h_line2),
            GrowFromCenter(dot1), GrowFromCenter(dot2),
            Write(label_a), Write(label_b),
            Write(label_fa), Write(label_fb)
        )
        self.play(Create(secant))
        self.play(Create(rectangles))
        
        # Scale and add title
        everything = Group(*self.mobjects)
        everything.scale(0.6).to_edge(LEFT)
        title = Text("Manim", font_size=72).next_to(everything, RIGHT).shift(DOWN * 0.7)
        self.add(title)
        
        self.wait(2)