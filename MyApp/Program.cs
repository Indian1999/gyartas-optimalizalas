using Google.OrTools.LinearSolver;

public class Program
{
    static void Main()
    {
        Solver solver = Solver.CreateSolver("SCIP");
        int[] igeny = { 22, 14, 18, 17, 15, 13, 15, 20 };
        // koltsegek matrix:        
        // model += 14*xgy1 + 25*xgy2 + 21*xgy3 + 20 * xgy4 + 21.5*xgy5 + 19*xgy6 + 17*xgy7 + 30*xgy8
        //  + 24*xr1 + 15*xr2 + 28*xr3 + 20*xr4 + 18.5*xr5 + 19.5*xr6 + 24*xr7 + 28*xr8
        double[,] koltseg = { { 14, 25, 21, 20, 21.5, 19, 17, 30 }, { 24, 15, 28, 20, 18.5, 19.5, 24, 28 } };
        Variable[] xgyar = solver.MakeIntVarArray(8, 0, double.PositiveInfinity);
        Variable[] xraktar = solver.MakeIntVarArray(8, 0, double.PositiveInfinity);

        Variable xgyk = solver.MakeIntVar(0, double.PositiveInfinity, "xgyk");
        Variable xrk = solver.MakeIntVar(0, double.PositiveInfinity, "xrk");
        Variable xk4 = solver.MakeIntVar(0, double.PositiveInfinity, "xk4");
        Variable xk5 = solver.MakeIntVar(0, double.PositiveInfinity, "xk5");
        Variable xk6 = solver.MakeIntVar(0, double.PositiveInfinity, "xk6");
        Variable xk = solver.MakeIntVar(0, double.PositiveInfinity, "xk");

        solver.Add(xgyar.Sum() + xgyk <= 100);
        solver.Add(xraktar.Sum() + xrk <= 45);
        for (int i = 0; i < 8; i++)
        {
            if (i == 3)
            {
                solver.Add(xgyar[i] + xraktar[i] + xk4 == igeny[i]);
            }
            else if (i == 4)
            {
                solver.Add(xgyar[i] + xraktar[i] + xk5 == igeny[i]);        
            }
            else if (i == 5)
            {
                solver.Add(xgyar[i] + xraktar[i] + xk6 == igeny[i]);
            }
            else
            {
                solver.Add(xgyar[i] + xraktar[i] == igeny[i]);
            }
        }

        solver.Add(xk <= 30);
        solver.Add(xgyk + xrk >= xk);
        solver.Add(xk4 + xk5 + xk6 <= xk);

        Objective objective = solver.Objective();
        for (int i = 0; i < 8; i++)
        {
            objective.SetCoefficient(xgyar[i], koltseg[0, i]);
            objective.SetCoefficient(xraktar[i], koltseg[1, i]);
        }
        objective.SetCoefficient(xgyk, 11.0);
        objective.SetCoefficient(xrk, 10.0);
        objective.SetCoefficient(xk, 2.0);
        objective.SetCoefficient(xk4, 6.0);
        objective.SetCoefficient(xk5, 5.0);
        objective.SetCoefficient(xk6, 5.0);
        objective.SetMinimization();

        Solver.ResultStatus status = solver.Solve();

        if (status == Solver.ResultStatus.OPTIMAL)
        {
            for (int i = 0; i < 8; i++)
            {
                Console.WriteLine($"gy{i + 1}: {(int)xgyar[i].SolutionValue()} db");
                Console.WriteLine($"r{i + 1}: {(int)xraktar[i].SolutionValue()} db");
            }
            Console.WriteLine($"gyk: {(int)xgyk.SolutionValue()} db");
            Console.WriteLine($"rk: {(int)xrk.SolutionValue()} db");
            Console.WriteLine($"k: {(int)xk.SolutionValue()} db");
            Console.WriteLine($"k4: {(int)xk4.SolutionValue()} db");
            Console.WriteLine($"k5: {(int)xk5.SolutionValue()} db");
            Console.WriteLine($"k6: {(int)xk6.SolutionValue()} db");
            Console.WriteLine($"Total cost: {solver.Objective().Value()} $");
        }
        else
        {
            Console.WriteLine("Nem talalhato optimalis megoldas.");
        }
    }
}