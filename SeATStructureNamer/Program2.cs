using System;
using System.Linq;
using ESIConnectionLibrary.Public_classes;
using ESIConnectionLibrary.PublicModels;
using Microsoft.EntityFrameworkCore;

namespace SeATStructureNamer
{
    public class Program2
    {
        public void Main(string connectionString)
        {
            LatestEndpoints esiLibrary = new LatestEndpoints("Seat Biomassed Character Script. Slack: Dusty Meg");

            CharacterInfo user = CharacterInfo(connectionString);

            SsoToken token = new SsoToken
            {
                AccessToken = user.RefreshToken.token,
                ExpiresIn = user.RefreshToken.expires_on,
                CharacterId = (int)user.character_id,
                UniverseScopesFlags = UniverseScopes.esi_universe_read_structures_v1
            };

            if (user.RefreshToken.expires_on <= DateTime.UtcNow.AddSeconds(30))
            {
                throw new NullReferenceException();
            }

            int structureCount = 0;

            using (LocalDbContext dbContext = new LocalDbContext(connectionString))
            {
                structureCount = dbContext.Structures.Count();
            }

            for (int i = 0; i < structureCount; i = i + 100)
            {
                CycleStructures(connectionString, user, esiLibrary, token, i);
            }
        }

        private static void CycleStructures(string connectionString, CharacterInfo user, LatestEndpoints esiLibrary, SsoToken token, int skip)
        {
            using (LocalDbContext dbContext = new LocalDbContext(connectionString))
            {
                foreach (UniverseStructures structure in dbContext.Structures.Skip(skip))
                {
                    if (structure.name == "Unknown Structure" &&
                        (structure.FailedCount == null || structure.FailedCount < 6))
                    {
                        try
                        {
                            if (user.RefreshToken.expires_on <= DateTime.UtcNow.AddMinutes(1))
                            {
                                user = CharacterInfo(connectionString);

                                if (user.RefreshToken.expires_on <= DateTime.UtcNow.AddMinutes(1))
                                {
                                    break;
                                }

                                token = new SsoToken
                                {
                                    AccessToken = user.RefreshToken.token,
                                    ExpiresIn = user.RefreshToken.expires_on,
                                    CharacterId = (int) user.character_id,
                                    UniverseScopesFlags = UniverseScopes.esi_universe_read_structures_v1
                                };
                            }

                            V2UniverseStructure esiStructure =
                                esiLibrary.UniverseEndpoints.Structure(token, structure.structure_id);

                            structure.name = esiStructure.Name;
                            structure.owner_id = esiStructure.OwnerId;
                            structure.solar_system_id = esiStructure.SolarSystemId;
                            structure.type_id = esiStructure.TypeId;
                            structure.x = esiStructure.Position.X;
                            structure.y = esiStructure.Position.Y;
                            structure.z = esiStructure.Position.Z;
                            structure.updated_at = DateTime.UtcNow;
                            structure.FailedCount = null;

                            Console.WriteLine($"Succeeded on {structure.structure_id}");
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine($"Failed on {structure.structure_id} with code {e.Message}");

                            if (structure.FailedCount == null)
                            {
                                structure.FailedCount = 1;
                            }
                            else
                            {
                                structure.FailedCount = structure.FailedCount + 1;
                            }

                            System.Threading.Thread.Sleep(TimeSpan.FromSeconds(5));
                        }
                    }
                }

                dbContext.SaveChanges();
            }
        }

        private static CharacterInfo CharacterInfo(string connectionString)
        {
            using (LocalDbContext dbContext = new LocalDbContext(connectionString))
            {
                CharacterInfo user = dbContext.Users
                    .Where(first =>
                        first.corporation_id == 98127387 &&
                        first.RefreshToken != null &&
                        first.RefreshToken.deleted_at == null)
                    .OrderByDescending(order => order.RefreshToken.expires_on)
                    .Include(include => include.RefreshToken)
                    .FirstOrDefault();
                return user;
            }
        }
    }
}