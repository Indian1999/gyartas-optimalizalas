using System.Numerics;
using System.Reflection.Metadata;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ObjectiveC;
using Google.OrTools.LinearSolver;

public class Program
{
    static void Main()
    {
        Solver model = Solver.CreateSolver("GLOP");

        if (model == null)
        {
            Console.WriteLine("Model could not be initialized.");
            return;
        }

        string[] comps = { "alpha", "beta", "gamma" };
        string[] weeks = { "week1", "week2", "week3", "week4" };

        int[] profits = { 350, 470, 610 };
        int[] inventory_cost = { 9, 10, 18 };
        int[] init_inventory = { 22, 42, 36 };

        int[,] lhs =
        {
            {1, 1, 0},
            {0, 0, 1},
            {10, 15, 20}
        };

        int[] rhs = { 120, 48, 2000 };

        (int min, int max)[,] forecast =
        {
            {(20, 60),(20,80),(20,120),(20, 140)},
            {(20, 40),(20,40),(20,40),(20, 40)},
            {(20, 50),(20,40),(20,30),(20, 70)}
        };

        // Döntési változók

        Variable[,] prod_vars = new Variable[weeks.Length, comps.Length];
        for (int i = 0; i < weeks.Length; i++)
        {
            for (int j = 0; j < comps.Length; j++)
            {
                prod_vars[i, j] = model.MakeNumVar(0, double.PositiveInfinity, $"M_{comps[j]}_{weeks[i]}");
            }
        }

        Variable[,] sales_vars = new Variable[weeks.Length, comps.Length];
        for (int i = 0; i < weeks.Length; i++)
        {
            for (int j = 0; j < comps.Length; j++)
            {
                //Console.WriteLine($"{i}, {j}");
                sales_vars[i, j] = model.MakeNumVar(forecast[j, i].min, forecast[j, i].max, $"S_{comps[j]}_{weeks[i]}");
            }
        }

        Variable[,] inventory_vars = new Variable[weeks.Length, comps.Length];
        for (int i = 0; i < weeks.Length; i++)
        {
            for (int j = 0; j < comps.Length; j++)
            {
                prod_vars[i, j] = model.MakeNumVar(0, double.PositiveInfinity, $"I_{comps[j]}_{weeks[i]}");
            }
        }

        // Célfüggvény

        LinearExpr objective = new LinearExpr();
        for (int i = 0; i < weeks.Length; i++)
        {
            for (int j = 0; j < comps.Length; j++)
            {
                objective += profits[j] * sales_vars[i, j] - inventory_cost[j];
            }
        }

        model.Maximize(objective);

        // Korlátozások
        for (int w = 0; w < weeks.Length; w++)
        {
            for (int i = 0; i < lhs.GetLength(0); i++)
            {
                for (int j = 0; j < lhs.GetLength(1); j++)
                {
                    model.Add(lhs[i, j] * prod_vars[w, j] <= rhs[i]);
                }
            }
        }
        // Material balance
        for (int i = 0; i < weeks.Length; i++)
        {
            for (int j = 0; j < comps.Length; j++)
            {
                if (i == 0)
                {
                    model.Add(init_inventory[j] + prod_vars[i, j] - sales_vars[i,j] == inventory_vars[i, j]);
                }
                else
                {
                    model.Add(inventory_vars[i - 1, j] + prod_vars[i, j] - sales_vars[i,j] == inventory_vars[i, j]);
                }
            }
        }


        // Megoldás

        Solver.ResultStatus status = model.Solve();

        if (status == Solver.ResultStatus.OPTIMAL)
        {
            Console.WriteLine($"Total profit: {model.Objective().Value()} $");
        }
        else
        {
            Console.WriteLine("Nem talalhato optimalis megoldas.");
        }
    }

}