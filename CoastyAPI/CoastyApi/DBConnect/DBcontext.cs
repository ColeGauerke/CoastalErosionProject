using Microsoft.EntityFrameworkCore;
using CoastyApi.Models;

namespace CoastalErosion.Data
{
    public class CoastalErosionDbContext : DbContext
    {
        public CoastalErosionDbContext(DbContextOptions<CoastalErosionDbContext> options) : base(options)
        {

        }
        public DbSet<EventReport> EventReports { get; set; }

    }
}