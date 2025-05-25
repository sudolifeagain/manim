from manim import *
import numpy as np

class LogoGeneration(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configuration parameters
        self.radius = 1.5
        self.inner_radius_ratio = 0.55
        self.circle_blue = BLUE_B
        self.circle_brown = "#8B4513"  # DARK_BROWN equivalent
        self.sphere_blue = BLUE_D
        self.sphere_brown = "#DEB887"  # LIGHT_BROWN equivalent
        self.interpolation_factor = 0.3
        self.run_time = 3
        
    def create_circle_mesh(self):
        """Create a circle with higher density for interpolation"""
        # Create multiple concentric circles for density
        circles = VGroup()
        num_circles = 5
        
        for i in range(num_circles):
            scale_factor = 0.2 + 0.8 * (i / (num_circles - 1))
            circle = Circle(radius=self.radius * scale_factor, color=self.circle_blue)
            circle.set_fill(opacity=0.3)
            circles.add(circle)
            
        # Add radial lines for mesh effect
        lines = VGroup()
        num_lines = 16
        for i in range(num_lines):
            angle = i * 2 * PI / num_lines
            line = Line(
                ORIGIN, 
                self.radius * np.array([np.cos(angle), np.sin(angle), 0]),
                color=self.circle_blue
            )
            lines.add(line)
            
        mesh = VGroup(circles, lines)
        return mesh
        
    def create_sphere_approximation(self):
        """Create a 3D-looking sphere using circles and shading"""
        # Main sphere outline
        main_circle = Circle(radius=self.radius, color=self.sphere_blue)
        main_circle.set_fill(self.sphere_blue, opacity=0.6)
        
        # Add shading circles to create 3D effect
        shading_circles = VGroup()
        
        # Highlight circle (top-left)
        highlight = Circle(radius=self.radius * 0.3, color=WHITE)
        highlight.set_fill(WHITE, opacity=0.4)
        highlight.shift(UP * 0.3 + LEFT * 0.3)
        
        # Shadow circles for depth
        for i in range(3):
            shadow_radius = self.radius * (0.8 - i * 0.2)
            shadow = Circle(radius=shadow_radius, color=self.sphere_blue)
            shadow.set_fill(self.sphere_blue, opacity=0.3 - i * 0.1)
            shadow.shift(DOWN * 0.1 * i + RIGHT * 0.1 * i)
            shading_circles.add(shadow)
            
        sphere = VGroup(main_circle, shading_circles, highlight)
        
        # Apply rotations to simulate 3D perspective
        sphere.rotate(-PI/7, axis=RIGHT)
        sphere.rotate(-PI/7, axis=OUT)
        
        return sphere
        
    def apply_color_conditions(self, mobject, brown_color):
        """Apply color conditions to simulate the original lambda functions"""
        # This is a simplified version since we can't easily access individual points
        # in modern Manim the same way as the old version
        
        # Create a gradient effect to simulate the original coloring
        mobject.set_color(brown_color)
        
        # Add inner black circle
        inner_circle = Circle(
            radius=self.inner_radius_ratio * self.radius,
            color=BLACK,
            fill_opacity=1
        )
        
        return VGroup(mobject, inner_circle)
        
    def construct(self):
        # Create initial circle mesh
        circle = self.create_circle_mesh()
        
        # Create target sphere
        sphere = self.create_sphere_approximation()
        
        # Create interpolated iris shape
        # Since we can't directly interpolate like the old version,
        # we'll create a hybrid shape
        iris_base = Circle(radius=self.radius, color=self.sphere_blue)
        iris_base.set_fill(self.sphere_blue, opacity=0.7)
        
        # Add some mesh lines from the circle
        iris_lines = VGroup()
        num_lines = 12
        for i in range(num_lines):
            angle = i * 2 * PI / num_lines
            line = Line(
                ORIGIN,
                self.radius * 0.8 * np.array([np.cos(angle), np.sin(angle), 0]),
                color=self.sphere_brown,
                stroke_width=1
            )
            iris_lines.add(line)
            
        iris = VGroup(iris_base, iris_lines)
        
        # Apply color conditions
        iris_colored = self.apply_color_conditions(iris, self.sphere_brown)
        circle_colored = self.apply_color_conditions(circle, self.circle_brown)
        
        # Create the name text
        name_text = Text("3Blue1Brown", color=GREY, font_size=36)
        name_text.shift(2 * DOWN)
        
        # Animation sequence
        self.add(circle_colored)
        self.wait(0.5)
        
        # Transform circle to iris
        self.play(
            Transform(circle_colored, iris_colored),
            run_time=self.run_time
        )
        
        # Add the name
        self.play(FadeIn(name_text))
        self.wait(2)
        
        # Optional: Add a final polishing effect
        final_logo = VGroup(circle_colored, name_text)
        self.play(
            final_logo.animate.scale(1.1).set_opacity(0.9),
            run_time=0.5
        )
        self.play(
            final_logo.animate.scale(1/1.1).set_opacity(1),
            run_time=0.5
        )
        
        self.wait(1)

# Alternative simpler version focusing on the core transformation
class SimpleLogoGeneration(Scene):
    def construct(self):
        # Simple circle to sphere transformation
        circle = Circle(radius=1.5, color=BLUE_B)
        circle.set_stroke(width=3)
        
        # Create wireframe effect
        lines = VGroup()
        for i in range(8):
            angle = i * PI / 4
            line = Line(
                1.5 * np.array([np.cos(angle), np.sin(angle), 0]),
                1.5 * np.array([np.cos(angle + PI), np.sin(angle + PI), 0]),
                color=BLUE_B
            )
            lines.add(line)
            
        circle_with_lines = VGroup(circle, lines)
        
        # Target sphere-like shape
        sphere = Circle(radius=1.5, color=BLUE_D)
        sphere.set_fill(BLUE_D, opacity=0.6)
        
        # Add 3D shading effect
        highlight = Circle(radius=0.4, color=WHITE)
        highlight.set_fill(WHITE, opacity=0.3)
        highlight.shift(UP * 0.4 + LEFT * 0.4)
        
        sphere_with_shading = VGroup(sphere, highlight)
        
        # Inner black circle (pupil)
        pupil = Circle(radius=0.8, color=BLACK, fill_opacity=1)
        
        # Text
        text = Text("3Blue1Brown", color=GREY, font_size=36)
        text.shift(2 * DOWN)
        
        # Animation
        self.add(circle_with_lines)
        self.wait(0.5)
        
        self.play(
            Transform(circle_with_lines, sphere_with_shading),
            run_time=3
        )
        
        self.add(pupil)
        self.play(FadeIn(text))
        self.wait(2)