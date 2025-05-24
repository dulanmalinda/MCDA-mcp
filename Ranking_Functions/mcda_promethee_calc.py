import math

class MCDACalcPromethee:
    def __init__(self, alternatives, criteria, weights, evaluations, maximize=True):
        """
        Initialize MCDACalcPromethee with decision problem parameters.
        
        Parameters:
        alternatives (list): List of alternative names.
        criteria (list): List of criterion names.
        weights (list): List of weights for each criterion.
        evaluations (list of lists): Matrix where evaluations[i][j] is the evaluation of 
                                   alternative i on criterion j.
        maximize (bool or list): True if all criteria are to be maximized, False if minimized,
                                or a list of booleans for each criterion.
        """
        self.alternatives = alternatives
        self.criteria = criteria
        self.weights = weights
        self.evaluations = evaluations
        self.n_alternatives = len(alternatives)
        self.n_criteria = len(criteria)
        self.maximize = [maximize] * self.n_criteria if isinstance(maximize, bool) else maximize
        
    def _compute_preference(self, diff, pref_func, p=0, q=0, s=0):
        """
        Compute preference value for a pair of alternatives on a criterion.
        
        Parameters:
        diff (float): Difference in evaluation between two alternatives.
        pref_func (str): Preference function type ('usual', 'u_shape', 'v_shape', 'level', 'linear', 'gaussian').
        p (float): Preference threshold for relevant functions.
        q (float): Indifference threshold for relevant functions.
        s (float): Gaussian parameter for gaussian function.
        
        Returns:
        float: Preference value between 0 and 1.
        """
        if pref_func == 'usual':
            return 1.0 if diff > 0 else 0.0
        elif pref_func == 'u_shape':
            return 1.0 if diff > q else 0.0
        elif pref_func == 'v_shape':
            return min(1.0, max(0.0, diff / p)) if p != 0 else (1.0 if diff > 0 else 0.0)
        elif pref_func == 'level':
            if diff <= q:
                return 0.0
            elif diff <= p:
                return 0.5
            else:
                return 1.0
        elif pref_func == 'linear':
            if diff <= q:
                return 0.0
            elif diff <= p:
                return (diff - q) / (p - q) if p != q else 0.0
            else:
                return 1.0
        elif pref_func == 'gaussian':
            return 1.0 - math.exp(-(diff ** 2) / (2 * s ** 2)) if diff > 0 else 0.0
        else:
            raise ValueError(f"Unknown preference function: {pref_func}")

    def _compute_preference_matrix(self, preference_functions, thresholds):
        """
        Compute preference matrix for all pairs of alternatives.
        
        Parameters:
        preference_functions (list): List of preference function types for each criterion.
        thresholds (list): List of tuples (q, p, s) for indifference, preference, and gaussian thresholds.
        
        Returns:
        list: Preference matrix [i][j] represents preference of alternative i over j.
        """
        preference_matrix = [[0.0] * self.n_alternatives for _ in range(self.n_alternatives)]
        
        for i in range(self.n_alternatives):
            for j in range(self.n_alternatives):
                if i != j:
                    preference_sum = 0.0
                    for k in range(self.n_criteria):
                        # Adjust difference based on maximize/minimize
                        diff = self.evaluations[i][k] - self.evaluations[j][k] if self.maximize[k] else self.evaluations[j][k] - self.evaluations[i][k]
                        q, p, s = thresholds[k]
                        preference = self._compute_preference(diff, preference_functions[k], p, q, s)
                        preference_sum += self.weights[k] * preference
                    preference_matrix[i][j] = preference_sum / sum(self.weights)
        return preference_matrix

    def promethee_1(self, preference_functions=None, thresholds=None):
        """
        PROMETHEE I: Partial ranking with positive and negative flows.
        
        Parameters:
        preference_functions (list): List of preference function types for each criterion.
        thresholds (list): List of tuples (q, p, s) for each criterion.
        
        Returns:
        tuple: (positive_flows, negative_flows) for each alternative.
        """
        if preference_functions is None:
            preference_functions = ['usual'] * self.n_criteria
        if thresholds is None:
            thresholds = [(0, 0, 0)] * self.n_criteria
            
        preference_matrix = self._compute_preference_matrix(preference_functions, thresholds)
        
        positive_flows = []
        negative_flows = []
        for i in range(self.n_alternatives):
            pos_flow = sum(preference_matrix[i][j] for j in range(self.n_alternatives) if j != i) / (self.n_alternatives - 1)
            neg_flow = sum(preference_matrix[j][i] for j in range(self.n_alternatives) if j != i) / (self.n_alternatives - 1)
            positive_flows.append(pos_flow)
            negative_flows.append(neg_flow)
        
        return positive_flows, negative_flows

    def promethee_2(self, preference_functions=None, thresholds=None):
        """
        PROMETHEE II: Complete ranking with net flow.
        
        Parameters:
        preference_functions (list): List of preference function types for each criterion.
        thresholds (list): List of tuples (q, p, s) for each criterion.
        
        Returns:
        list: Net flows for each alternative (positive - negative).
        """
        pos_flows, neg_flows = self.promethee_1(preference_functions, thresholds)
        return [pos - neg for pos, neg in zip(pos_flows, neg_flows)]

    def promethee_3(self, preference_functions=None, thresholds=None, alpha=0.1):
        """
        PROMETHEE III: Ranking with intervals based on net flow and uncertainty.
        
        Parameters:
        preference_functions (list): List of preference function types for each criterion.
        thresholds (list): List of tuples (q, p, s) for each criterion.
        alpha (float): Parameter for interval width.
        
        Returns:
        list: List of tuples (net_flow, lower_bound, upper_bound) for each alternative.
        """
        net_flows = self.promethee_2(preference_functions, thresholds)
        # Simplified interval estimation (using alpha as a scaling factor for uncertainty)
        return [(flow, flow - alpha, flow + alpha) for flow in net_flows]

    def promethee_4(self, preference_functions=None, thresholds=None):
        """
        PROMETHEE IV: Continuous case (simplified as discrete with normalized flows).
        
        Parameters:
        preference_functions (list): List of preference function types for each criterion.
        thresholds (list): List of tuples (q, p, s) for each criterion.
        
        Returns:
        list: Normalized net flows for each alternative.
        """
        net_flows = self.promethee_2(preference_functions, thresholds)
        max_flow = max(net_flows, default=1.0)
        min_flow = min(net_flows, default=-1.0)
        flow_range = max_flow - min_flow if max_flow != min_flow else 1.0
        return [(flow - min_flow) / flow_range for flow in net_flows]

    def promethee_5(self, preference_functions=None, thresholds=None, constraints=None):
        """
        PROMETHEE V: Multi-criteria with constraints (simplified as filtering by constraints).
        
        Parameters:
        preference_functions (list): List of preference function types for each criterion.
        thresholds (list): List of tuples (q, p, s) for each criterion.
        constraints (list): List of boolean constraints per alternative (True if feasible).
        
        Returns:
        list: Net flows for feasible alternatives, None for infeasible ones.
        """
        if constraints is None:
            constraints = [True] * self.n_alternatives
        net_flows = self.promethee_2(preference_functions, thresholds)
        return [flow if constraints[i] else None for i, flow in enumerate(net_flows)]

    def promethee_6(self, preference_functions=None, thresholds=None):
        """
        PROMETHEE VI: Human brain model with hesitation (simplified as weighted flows).
        
        Parameters:
        preference_functions (list): List of preference function types for each criterion.
        thresholds (list): List of tuples (q, p, s) for each criterion.
        
        Returns:
        tuple: (min_flows, central_flows, max_flows) for each alternative.
        """
        pos_flows, neg_flows = self.promethee_1(preference_functions, thresholds)
        central_flows = [(pos + neg) / 2 for pos, neg in zip(pos_flows, neg_flows)]
        min_flows = [min(pos, neg) for pos, neg in zip(pos_flows, neg_flows)]
        max_flows = [max(pos, neg) for pos, neg in zip(pos_flows, neg_flows)]
        return min_flows, central_flows, max_flows