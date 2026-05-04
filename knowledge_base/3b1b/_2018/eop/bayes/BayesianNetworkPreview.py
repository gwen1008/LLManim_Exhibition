# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 展示貝葉斯網絡中從一個節點開始，訊息沿著邊緣向相鄰節點傳播的動畫過程。


from manim import *
import itertools as it

class BayesianNetworkPreview(Scene):
    def construct(self):
        self.add_network()
        self.show_propogation(self.network.nodes[0])
        self.show_propogation(self.network.nodes[-1])

    def add_network(self):
        radius = MED_SMALL_BUFF
        node = Circle(color=WHITE, radius=radius)
        node.shift(2*DOWN)
        nodes = VGroup(*[
            node.copy().shift(x*RIGHT + y*UP)
            for x, y in [
                (-1, 0),  
                (1, 0),
                (-2, 2),
                (0, 2),
                (2, 2),
                (-2, 4),
                (0, 4),
            ]
        ])
        for node in nodes:
            node.children = VGroup()
            node.parents = VGroup()
            node.outgoing_edges = VGroup()
        edge_index_pairs = [
            (2, 0),
            (3, 0),
            (3, 1),
            (4, 1),
            (5, 2),
            (6, 3),
        ]
        edges = VGroup()
        for i1, i2 in edge_index_pairs:
            n1, n2 = nodes[i1], nodes[i2]
            edge = Arrow(
                n1.get_center(), 
                n2.get_center(),
                buff=radius,
                color=WHITE,
            )
            n1.outgoing_edges.add(edge)
            edges.add(edge)
            n1.children.add(n2)
            n2.parents.add(n1)

        network = VGroup(nodes, edges)
        network.nodes = nodes
        network.edges = edges
        self.add(network)
        self.network = network

    def show_propogation(self, node):
        self.set_network_fills()
        all_ghosts = VGroup()
        curr_nodes = [node]
        covered_nodes = set()
        self.play(GrowFromCenter(node.fill))
        self.remove(node.fill)
        while curr_nodes:
            next_nodes = set([])
            anims = []
            for node in curr_nodes:
                node.ghost = node.fill.copy().set_opacity(0.5)  # .fade() 替換
                self.add(node.ghost)
                all_ghosts.add(node.ghost)
                connected_nodes = [n for n in it.chain(node.children, node.parents) if n not in covered_nodes]
                for next_node in connected_nodes:
                    if next_node in covered_nodes:
                        continue
                    next_nodes.add(next_node)
                    anims.append(Transform(
                        node.fill.copy(), next_node.fill,
                        remover=True
                    ))
                if len(connected_nodes) == 0:
                    anims.append(FadeOut(node.fill))
            if anims:
                self.play(*anims)
            covered_nodes.update(curr_nodes)
            curr_nodes = list(next_nodes)
        self.wait()
        self.play(FadeOut(all_ghosts))

    def set_network_fills(self):
        for node in self.network.nodes:
            node.fill = self.get_fill(node)

    def get_fill(self, node):
        fill = node.copy()
        fill.set_fill(YELLOW, opacity=1)
        fill.set_stroke(width=0)
        return fill
