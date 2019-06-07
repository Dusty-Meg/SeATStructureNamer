using System;
using Microsoft.EntityFrameworkCore;
using Pomelo.EntityFrameworkCore.MySql.Infrastructure;

namespace SeATStructureNamer
{
    public class LocalDbContext : DbContext
    {
        private string ConnectionString { get; set; }

        public LocalDbContext(string connectionString)
        {
            ConnectionString = connectionString;
        }

        public virtual DbSet<CharacterInfo> Users { get; set; }
        public virtual DbSet<UniverseStructures> Structures { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseMySql(ConnectionString
                    , builder =>
                    {
                        builder.ServerVersion(new Version(10, 3, 13), ServerType.MariaDb);
                    });
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<RefreshTokens>(entity =>
            {
                entity.HasKey(key => key.character_id);
                entity.ToTable("refresh_tokens");
            });

            modelBuilder.Entity<CharacterInfo>(entity =>
            {
                entity.HasKey(key => key.character_id);
                entity.ToTable("character_infos");

                entity.HasOne(one => one.RefreshToken).WithOne(one => one.User).HasForeignKey<RefreshTokens>(rt => rt.character_id);
            });

            modelBuilder.Entity<UniverseStructures>(entity =>
            {
                entity.HasKey(key => key.structure_id);
                entity.ToTable("universe_structures");
            });
        }
    }
}