using System.Numerics;
using System.Reflection.Metadata;
using System.Runtime.InteropServices.ObjectiveC;
using Google.OrTools.LinearSolver;

public class Program
{
    static void Main()
    {
        Solver solver = Solver.CreateSolver("SCIP");
        int[,] koltseg =
        {
            {0, 0, 25, 100, 5, 25, 100, 100},
            {5, 100, 5, 0, 25, 100, 25, 100},
            {5, 5, 100, 5, 5, 0, 25, 100},
            {0, 5, 25, 25, 25, 0, 100, 25},
            {100, 100, 100, 25, 5, 25, 5, 5},
            {100, 100, 0, 25, 25, 25, 5, 0},
            {25, 25, 25, 100, 100, 100, 0, 5},
            {25, 5, 100, 25, 0, 100, 100, 0}
        };

        int n = koltseg.GetLength(0);
        int m = koltseg.GetLength(1);

        Variable[,] x = new Variable[n, m];
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                x[i, j] = solver.MakeBoolVar($"x[{i},{j}]");
            }
        }

        for (int i = 0; i < n; i++)
        {
            // lowerbound, upperbound, name
            Constraint rowC = solver.MakeConstraint(1, 1, $"row_{i}");
            Constraint colC = solver.MakeConstraint(1, 1, $"col_{i}");
            for (int j = 0; j < m; j++)
            {
                rowC.SetCoefficient(x[i, j], 1);
                colC.SetCoefficient(x[j, i], 1);
            }
        }

        Objective objective = solver.Objective();
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                objective.SetCoefficient(x[i,j], koltseg[i,j]);
            }
        }
        objective.SetMinimization();

        Solver.ResultStatus status = solver.Solve();

        if (status == Solver.ResultStatus.OPTIMAL)
        {
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < m; j++)
                {
                    Console.Write($"{(int)x[i,j].SolutionValue()}");
                }
                Console.Write("\n");
            }
            Console.Write($"A minimális költség: {solver.Objective().Value()}");
        }
    }

}