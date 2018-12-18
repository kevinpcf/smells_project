module.exports = {
  rules: {
    'no-reassign': function(context) {

      function isValidTarget(node) {
        if (node.type === 'ThisExpression') {
          return true;
        }
        if (node.type === 'Identifier') {
          var exceptions = context.options.concat('module', 'exports');
          if (exceptions.indexOf(node.name) !== -1) {
            return true;
          }
        }
        if (node.type === 'MemberExpression') {
          return isValidTarget(node.object);
        }
        return false;
      }

      return {
        AssignmentExpression: function(node) {
          if (!isValidTarget(node.left)) {
            context.report(node, 'variable reassignment');
          }
        }
      };
    }
  },
  rulesConfig: {
    'no-reassign': [1, 'self']
  }
}
