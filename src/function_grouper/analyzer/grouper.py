"""Function grouping analysis using connected components."""


import networkx as nx

from function_grouper.models import CallGraph, FunctionGroup


class Grouper:
    """Identifies independent function groups using connected component analysis."""

    def find_independent_groups(self, call_graph: CallGraph) -> list[FunctionGroup]:
        """Find independent function groups in the call graph.

        Args:
            call_graph: CallGraph to analyze

        Returns:
            List of FunctionGroup objects representing connected components
        """
        if len(call_graph) == 0:
            return []

        # Get the NetworkX graph (directed)
        digraph = call_graph.get_networkx_graph()

        # Convert to undirected for connected components
        # (functions are in same group if connected by ANY path)
        undirected = digraph.to_undirected()

        # Find connected components
        components = list(nx.connected_components(undirected))

        # Create FunctionGroup objects
        groups: list[FunctionGroup] = []
        for group_id, component in enumerate(components):
            func_list = list(component)

            # Create the group
            group = FunctionGroup(
                group_id=group_id,
                functions=func_list,
            )

            # Compute statistics for this group
            self._compute_group_statistics(group, call_graph, digraph)

            groups.append(group)

        return groups

    def _compute_group_statistics(
        self,
        group: FunctionGroup,
        call_graph: CallGraph,
        digraph: nx.DiGraph,
    ) -> None:
        """Compute statistics for a function group.

        Args:
            group: FunctionGroup to update
            call_graph: Complete call graph
            digraph: NetworkX directed graph
        """
        # Count internal edges (edges within the group)
        internal_edges = 0
        for func in group.functions:
            callees = call_graph.get_callees(func)
            for callee in callees:
                if callee in group.functions:
                    internal_edges += 1

        group.internal_edges = internal_edges

        # Count external edges (edges to/from outside the group)
        external_edges = 0
        for func in group.functions:
            # Check outgoing edges
            callees = call_graph.get_callees(func)
            for callee in callees:
                if callee not in group.functions:
                    external_edges += 1

            # Check incoming edges
            callers = call_graph.get_callers(func)
            for caller in callers:
                if caller not in group.functions:
                    external_edges += 1

        group.external_edges = external_edges

        # Determine if independent (no external edges)
        group.is_independent = (external_edges == 0)

        # Check for cycles within the group
        subgraph = digraph.subgraph(group.functions)
        try:
            nx.find_cycle(subgraph)
            group.has_cycles = True
        except nx.NetworkXNoCycle:
            group.has_cycles = False
