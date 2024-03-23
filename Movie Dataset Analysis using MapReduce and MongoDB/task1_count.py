from mrjob.job import MRJob

class MovieFrequency(MRJob):
    def configure_args(self):
        super(MovieFrequency, self).configure_args()
        self.add_passthru_arg('--output-format', default='normal', choices=['normal', 'custom'])

    def mapper(self, _, line):
        year, company = line.split('\t')
        yield (year, company), 1

    def reducer(self, key, values):
        year, company = key
        frequency = sum(values)
        
        #if self.options.output_format == 'normal':
        yield f'{year}, {company}',frequency
        #elif self.options.output_format == 'custom':
        #    yield year, company, frequency

if __name__ == '__main__':
    MovieFrequency.run()
