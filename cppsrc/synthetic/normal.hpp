class SyntheticNormal
{
public:
    SyntheticNormal()
    {
    }
    float *run(float *calculation, float *source, float *additions) //RGBA // RGBA
    {

        //cout << "source" << source[0] << " " << source[1] << " " << source[2] << " " << source[3] << endl;
        //cout << "additions" << additions[0] << " " << additions[1] << " " << additions[2] << " " << additions[3] << endl;

        //all_calculation[:, :, 3] = source[:, :, 3] * (np01 - additions[:, :, 3]) + additions[:, :, 3]
        calculation[3] = source[3] * (1 - additions[3]) + additions[3];

        //all_calculation[:, :, 3] = source[:, :, 3] * (np01 - additions[:, :, 3]) + additions[:, :, 3]

        for (int i = 0; i < 3; i++)
        {
            //source[:, :, 3] * (np01 - additions[:, :, 3]) * source[:, :, i] + additions[:, :, 3] * additions[:, :, i]

            calculation[i] = source[3] * (1 - additions[3]) * source[i] + additions[3] * additions[i];

            //all_calculation[:, :, i] = source[:, :, 3] * (np01 - additions[:, :, 3]) * source[:, :, i] + additions[:, :, 3] * additions[:, :, i]
            if (calculation[3] == 0)
            {
                calculation[i] = 0;
            }
            else
            {
                calculation[i] /= calculation[3];
            }
        }

        //cout << "calculation" << calculation[0] << " " << calculation[1] << " " << calculation[2] << " " << calculation[3] << endl;

        return &calculation[0];
    }
};