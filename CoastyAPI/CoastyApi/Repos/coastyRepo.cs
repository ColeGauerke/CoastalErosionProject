using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using CoastyApi.Models;
using CoastyApi.Contracts;
using Microsoft.EntityFrameworkCore;
using CoastalErosion.Data;
using MySql.Data.MySqlClient;  
using System.Data;
using Microsoft.VisualBasic;


namespace CoastyApi.Repos
{
    public class TestRepo : ICoastyContract
    {
        private readonly CoastalErosionDbContext _db;
        public TestRepo(CoastalErosionDbContext db)
        {
            _db = db;
        }
        public Task<string> GetNameTest(User user)
        {
            if (user.name == null)
            {
                return Task.FromResult("No Name Given");
            }
            else
            {
                return Task.FromResult(user.name);
            }
        }

        public async Task<object> GetAvgWaterLevels(WaterLvlRequest request)
        {
            var results = new List<Dictionary<string, object>>();
            var connection = _db.Database.GetDbConnection();
            try
            {
                await connection.OpenAsync();

                using (var command = connection.CreateCommand())
                {
                    command.CommandText = "GetVerifiedWaterLevels";
                    command.CommandType = CommandType.StoredProcedure;
                    command.Parameters.Add(new MySqlParameter("p_time_period", request.period ?? "day"));
                    command.Parameters.Add(new MySqlParameter("p_city", request.city ?? ""));
                    command.Parameters.Add(new MySqlParameter("p_state", request.state ?? ""));
                    command.Parameters.Add(new MySqlParameter("p_start_date",string.IsNullOrEmpty(request.startDate) ? DBNull.Value : request.startDate));
                    command.Parameters.Add(new MySqlParameter("p_end_date",string.IsNullOrEmpty(request.endDate) ? DBNull.Value : request.endDate));

                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            var row = new Dictionary<string, object>();
                            for (int i = 0; i < reader.FieldCount; i++)
                            {
                                row[reader.GetName(i)] = reader.IsDBNull(i) ? null : reader.GetValue(i);
                            }
                            results.Add(row);
                        }
                    }
                }
            }
            finally
            {
                await connection.CloseAsync();
            }

            return results;
        }
        
        public async Task<object> GetRisks(string city, string year)
        {
            var results = new List<Dictionary<string, object>>();
            var connection = _db.Database.GetDbConnection();
            try
            {
                await connection.OpenAsync();
                using (var command = connection.CreateCommand())
                {
                    command.CommandText = "GetRisks";
                    command.CommandType = CommandType.StoredProcedure;

                    command.Parameters.Add(new MySqlParameter("city", city ?? "New Orleans"));
                    command.Parameters.Add(new MySqlParameter("yar", year));
                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            var row = new Dictionary<string, object>();
                            for (int i = 0; i < reader.FieldCount; i++)
                            {
                                row[reader.GetName(i)] = reader.IsDBNull(i) ? null : reader.GetValue(i);
                            }
                            results.Add(row);
                        }
                    }
                }
            }
            finally
            {
                await connection.CloseAsync();
            }
            
            return results;
        }
    }
}