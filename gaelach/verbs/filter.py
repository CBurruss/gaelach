from gaelach.core.symbolic import SymbolicAttr, ColumnExpression, BinaryOperation

# Define the filter() verb
def filter(*conditions):
    """
    Filter rows based on boolean conditions.
    
    *conditions: One or more boolean expressions using _
                 Multiple conditions are combined with AND logic
    
    Returns a function that performs the filtering on a DataFrame.
    """
    def _filter(df):
        # Evaluate each condition to get boolean Series
        masks = []
        for condition in conditions:
            if isinstance(condition, ColumnExpression):
                masks.append(condition._evaluate(df))
            elif isinstance(condition, BinaryOperation):
                masks.append(condition._evaluate(df))
            else:
                # Already a boolean Series
                masks.append(condition)
        
        # Combine all conditions with AND logic
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask = combined_mask & mask
        
        # Use boolean indexing to filter rows
        return df[combined_mask]
    
    return _filter