class ExecutionTrace:
    def __init__(self):
        self.iterations = []
    
    def record_iteration(self, iteration_id, concrete_inputs, return_value, exception=None, branch_trace=None):
        """Record an execution iteration"""
        iteration_data = {
            "iteration_id": iteration_id,
            "concrete_inputs": concrete_inputs,
            "return_value": return_value,
            "exception": str(exception) if exception else None,
            "branch_trace": branch_trace
        }
        self.iterations.append(iteration_data)
    
    def get_iterations(self):
        """Get all recorded iterations"""
        return self.iterations
    
    def to_dict(self):
        """Convert trace to dictionary"""
        return {
            "iterations": self.iterations
        }
