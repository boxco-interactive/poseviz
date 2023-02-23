import poseviz.components.connected_points_viz
import poseviz.mayavi_util
import poseviz.colors as colors


class SkeletonsViz:
    def __init__(self, joint_info, left_color, mid_color, right_color, point_color, scale_factor,
                 high_quality=False):
        opacity = 0.7
        joint_names, joint_edges = joint_info
        edge_colors = dict(left=left_color, mid=mid_color, right=right_color, fist=(1.0,0.0,0.0), head=(0.940, 0.0658, 0.765))
        point_colors = dict(left=point_color, mid=point_color, right=point_color, fist=(1.0,0.0,0.0), head=(0.940, 0.0658, 0.765))
        sides = ('left', 'mid', 'right', 'fist', 'head')

        def edge_side(edge):
            s1 = joint_side(edge[0])
            s2 = joint_side(edge[1])
            if s1 == 'left' or s2 == 'left':
                return 'left'
            elif s1 == 'right' or s2 == 'right':
                return 'right'
            else:
                return 'mid'

        def joint_side(joint):
            name = joint_names[joint].lower()
            if name.endswith('head'):
                return 'head'
            if name.endswith('wrist'):
                return 'fist'
            elif name.startswith('l'):
                return 'left'
            elif name.startswith('r'):
                return 'right'
            else:
                return 'mid'
            
        # compute join sides
        joints_of_joint_side = {}
        for side in sides:
            joints_of_joint_side[side] = [joint_name for joint_name in joint_names if joint_side(joint_names.index(joint_name)) == side]

        scale_factor_of_joint_side = {'left': scale_factor, 'mid': scale_factor, 'right': scale_factor, 'fist': 2*scale_factor, 'head': 2.5*scale_factor}
        
        # this is where the color stuff happens
        self.pointsets = {
            side: poseviz.components.connected_points_viz.ConnectedPoints(
                point_colors[side], edge_colors[side], 'sphere', scale_factor_of_joint_side[side], opacity, opacity,
                joints_of_joint_side[side], high_quality)
            for side in sides}

        self.edges_per_side = {
            side: [e for e in joint_edges if edge_side(e) == side]
            for side in sides}

        self.indices_per_side = {
            side: sorted(
                set([index for edge in self.edges_per_side[side] for index in edge]) |
                set([index for index, name in enumerate(joint_names) if joint_side(index) == side])
            )
            for side in sides}

        def index_within_side(global_index, side):
            return self.indices_per_side[side].index(global_index)

        self.edges_within_side = {
            side: [(index_within_side(i, side), index_within_side(j, side))
                   for i, j in self.edges_per_side[side]]
            for side in sides}

    def update(self, poses):
        mayavi_poses = [poseviz.mayavi_util.world_to_mayavi(pose) for pose in poses]
        for side, pointset in self.pointsets.items():
            pointset.clear()
            for coords in mayavi_poses:
                pointset.add_points(
                    coords[self.indices_per_side[side]], self.edges_within_side[side],
                    show_isolated_points=True)
            pointset.update()
