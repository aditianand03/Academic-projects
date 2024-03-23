from mrjob.job import MRJob

class BucketSortMRJob(MRJob):
    def configure_args(self):
        super(BucketSortMRJob, self).configure_args()
        self.add_passthru_arg('--num-top', default=5, type=int,
                              help='Number of top entries to include in the output')

    def mapper(self, _, line):
        year_company, count = line.strip().split('\t')
        yield None, (int(count), year_company)

    def reducer(self, _, values):
        
        sorted_values = sorted(values, reverse=True)

        for i, (count, year_company) in enumerate(sorted_values):
            yield f'{year_company}', count
            

if __name__ == '__main__':
    BucketSortMRJob.run()
