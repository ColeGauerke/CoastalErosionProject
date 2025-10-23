using Microsoft.EntityFrameworkCore;

namespace CoastalErosion.Data
{
    public class CoastalErosionDbContext : DbContext
    {
        public CoastalErosionDbContext(DbContextOptions<CoastalErosionDbContext> options) : base(options)
        {
            
        }
    }
}