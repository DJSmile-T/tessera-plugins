#include "picture_frame.h"
#include <string>

namespace esphome::picture_frame {

using tessera::Font;
namespace ui = tessera::ui;

// The tile: one place for a picture over the whole card, the name in its corner. The address comes from the option, or
// from the entity's own picture (its entity_picture) when the option is empty. On a board that shows no pictures the
// tile says so, and stays a plain card otherwise.
class PictureTile : public tessera::Tile {
 public:
  explicit PictureTile(const tessera::Plugin *plugin) : plugin_(plugin) {}

  void create(const tessera::TileContext &c) override {
    url_ = c.options["url"] | "";
    contain_ = std::string(c.options["fit"] | "cover") == "contain";
    caption_ = c.options["caption"] | true;
    name_ = c.name;
    if (ui::pictures()) {
      place_ = ui::picture(c.parent);
      lv_obj_set_size(place_, c.width, c.height);
      lv_obj_set_pos(place_, 0, 0);
    }
    // The name in the corner, or, without pictures, the word that says why there is none.
    label_ = ui::label(c.parent, Font::BODY, place_ ? theme::INK : theme::MUTED);
    lv_obj_set_width(label_, c.width);
    lv_obj_set_pos(label_, 0, place_ ? c.height - ui::line_height(Font::BODY) : (c.height - ui::line_height(Font::BODY)) / 2);
    if (!place_) lv_obj_set_style_text_align(label_, LV_TEXT_ALIGN_CENTER, 0);
    ui::set_text(label_, place_ ? (caption_ ? name_ : "") : plugin_->text("no_picture"));
  }

  void on_state(JsonObjectConst data) override {
    // The entity's own picture, when the tile has an entity and no address of its own.
    const std::string own = data["attributes"]["entity_picture"] | "";
    if (place_) ui::set_picture(place_, url_.empty() ? own : url_, contain_ ? tessera::Fit::CONTAIN : tessera::Fit::COVER);
  }

  void on_theme() override { ui::set_color(label_, place_ ? theme::INK : theme::MUTED); }

 private:
  const tessera::Plugin *plugin_;
  std::string url_, name_;
  bool contain_ = false, caption_ = true;
  lv_obj_t *place_{}, *label_{};
};

void PictureFrame::setup() {
  add_tile("picture", [this]() { return new PictureTile(this); });
}

}  // namespace esphome::picture_frame
