require 'nominatim'
require 'logger'
require 'active_support/all'
require_relative './place'

$logger = Logger.new(STDOUT)

module Nominatim
  def self.search_with_alt_names(q)
    search = Nominatim::Search.new
    search.search_with_alt_names(q)
    search
  end
end

module Nominatim
  class Search
    def search_with_alt_names(q)
      @criteria[:q] = q
      @criteria[:namedetails] = 1

      self
    end
  end
end

def save_data_from_osm
  Place.all.each do |p|
    $logger.info("Getting place information for #{p.name}")
    place = Nominatim.search(ActiveSupport::Inflector.transliterate(p.name)).limit(1).address_details(true).first

    if place
      $logger.debug("Updating place data for #{p.id} with #{place}")
      p.osm_id           = place.osm_id
      p.lat              = place.lat
      p.long             = place.lon
      p.osm_class        = place.class
      p.osm_type         = place.type
      p.osm_display_name = place.display_name
      p.osm_importance   = place.instance_variable_get(:@attrs)[:importance]
      p.address          = place.address.instance_variable_get(:@attrs)
      p.osm_importance   = place.instance_variable_get(:@attrs)[:importance]
      p.alt_names        = place.instance_variable_get(:@attrs)[:namedetails]

      p.save
    else
      $logger.error("No data found for #{p.name}")
    end
  end
end
