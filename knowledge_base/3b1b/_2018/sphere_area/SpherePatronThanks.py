# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示由社群資助的感謝名單，以黃色標題和分欄動畫呈現贊助者姓名。


from manim import *
import random

class SpherePatronThanks(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.specific_patrons = [
            "1stViewMaths",
            "Adrian Robinson",
            "Alexis Olson",
            "Ali Yahya",
            "Andrew Busey",
            "Ankalagon",
            "Antonio Juarez",
            "Art Ianuzzi",
            "Arthur Zey",
            "Awoo",
            "Bernd Sing",
            "Boris Veselinovich",
            "Brian Staroselsky",
            "brian tiger chow",
            "Brice Gower",
            "Britt Selvitelle",
            "Burt Humburg",
            "Carla Kirby",
            "Charles Southerland",
            "Chris Connett",
            "Christian Kaiser",
            "Clark Gaebel",
            "Cooper Jones",
            "Danger Dai",
            "Dave B",
            "Dave Kester",
            "dave nicponski",
            "David Clark",
            "David Gow",
            "Delton Ding",
            "Devarsh Desai",
            "Devin Scott",
            "eaglle",
            "Eric Younge",
            "Eryq Ouithaqueue",
            "Evan Phillips",
            "Federico Lebron",
            "Florian Chudigiewitsch",
            "Giovanni Filippi",
            "Graham",
            "Hal Hildebrand",
            "J",
            "Jacob Magnuson",
            "Jameel Syed",
            "James Hughes",
            "Jan Pijpers",
            "Jason Hise",
            "Jeff Linse",
            "Jeff Straathof",
            "Jerry Ling",
            "John Griffith",
            "John Haley",
            "John Shaughnessy",
            "John V Wertheim",
            "Jonathan Eppele",
            "Jonathan Wilson",
            "Joseph John Cox",
            "Joseph Kelly",
            "Juan Benet",
            "Julian Pulgarin",
            "Kai-Siang Ang",
            "Kanan Gill",
            "Kaustuv DeBiswas",
            "L0j1k",
            "Linh Tran",
            "Luc Ritchie",
            "Ludwig Schubert",
            "Lukas -krtek.net- Novy",
            "Lukas Biewald",
            "Magister Mugit",
            "Magnus Dahlström",
            "Magnus Lysfjord",
            "Mark B Bahu",
            "Markus Persson",
            "Mathew Bramson",
            "Mathias Jansson",
            "Matt Langford",
            "Matt Roveto",
            "Matt Russell",
            "Matthew Cocke",
            "Maurício Collares",
            "Mehdi Razavi",
            "Michael Faust",
            "Michael Hardel",
            "MrSneaky",
            "Mustafa Mahdi",
            "Márton Vaitkus",
            "Nathan Jessurun",
            "Nero Li",
            "Oliver Steele",
            "Omar Zrien",
            "Peter Ehrnstrom",
            "Peter Mcinerney",
            "Quantopian",
            "Randy C. Will",
            "Richard Burgmann",
            "Ripta Pasay",
            "Rish Kundalia",
            "Robert Teed",
            "Roobie",
            "Roy Larson",
            "Ryan Atallah",
            "Ryan Williams",
            "Scott Walter, Ph.D.",
            "Sindre Reino Trosterud",
            "soekul",
            "Solara570",
            "Song Gao",
            "Steven Soloway",
            "Stevie Metke",
            "Ted Suzman",
            "Valeriy Skobelev",
            "Vassili Philippov",
            "Xavier Bernard",
            "Yana Chernobilsky",
            "Yaw Etse",
            "YinYangBalance Asia",
            "Zach Cardwell",
        ]

    def construct(self):
        self.add_title()
        self.show_columns()

    def add_title(self):
        title = Text("Funded by the community, with special thanks to:")
        title.set_color(YELLOW)
        title.to_edge(UP)
        underline = Line(LEFT, RIGHT)
        underline.set_width(title.width + MED_SMALL_BUFF)
        underline.next_to(title, DOWN, buff=SMALL_BUFF)
        title.add(underline)

        self.add(title)
        self.title = title

    def show_columns(self):
        random.seed(1)
        random.shuffle(self.specific_patrons)
        patrons = VGroup(*[
            Text(name)
            for name in self.specific_patrons
        ])
        columns = VGroup()
        column_size = 15
        for n in range(0, len(patrons), column_size):
            column = patrons[n:n + column_size]
            column.arrange(
                DOWN,
                aligned_edge=LEFT
            )
            columns.add(column)
        columns.set_height(6)
        for group in columns[:4], columns[4:]:
            for k, column in enumerate(group):
                column.move_to(
                    6.5 * LEFT + 3.75 * k * RIGHT + 2.5 * UP,
                    aligned_edge=UL
                )

        self.add(columns[:4])
        self.wait()
        for k in range(4):
            self.play(
                FadeOut(columns[k]),
                FadeIn(columns[k + 4]),
            )
        self.wait()
