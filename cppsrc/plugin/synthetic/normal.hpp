class SyntheticNormal
{
public:
    SyntheticNormal()
    {
    }
    void run(int *calculation, int *source, int *additions) //RGBA // RGBA
    {
        //all_calculation[:, :, 3] = source[:, :, 3] * (np01 - additions[:, :, 3]) + additions[:, :, 3]
        calculation[3] = source[3] * (1 - additions[3]) + additions[3];

        for (int i = 0; i < 3; i++)
        {
            //source[:, :, 3] * (np01 - additions[:, :, 3]) * source[:, :, i] + additions[:, :, 3] * additions[:, :, i]
            calculation[i] = source[3] * (1 - additions[3]) * source[i] + additions[3] * additions[i];

            if (calculation[3] != 0)
            {
                calculation[i] /= calculation[3];
            }
        }
    }
};