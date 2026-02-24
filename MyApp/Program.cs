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

        solver.Add(xgyar.Sum() <= 100);
        solver.Add(xraktar.Sum() <= 45);
        for (int i = 0; i < 8; i++)
        {
            solver.Add(xgyar[i] + xraktar[i] == igeny[i]);
        }
        
        Objective objective = solver.Objective();
        for (int i = 0; i < 8; i++)
        {
            objective.SetCoefficient(xgyar[i], koltseg[0, i]);
            objective.SetCoefficient(xraktar[i], koltseg[1, i]);
        }
        objective.SetMinimization();

        Solver.ResultStatus status = solver.Solve();

        if (status == Solver.ResultStatus.OPTIMAL)
        {
            for (int i = 0; i < 8; i++)
            {
                Console.WriteLine($"gy{i + 1}: {(int)xgyar[i].SolutionValue()} db");
                Console.WriteLine($"r{i + 1}: {(int)xraktar[i].SolutionValue()} db");
            }
            Console.WriteLine($"Total cost: {solver.Objective().Value()} $");
        }
        else
        {
            Console.WriteLine("Nem talalhato optimalis megoldas.");
        }
    }
}