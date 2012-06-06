
"""Test that the ChamplainLabels are behaving."""

from gi.repository import Clutter, Champlain

from gg.common import Widgets, selected
from gg.photos import Photograph
from gg.label import Label, selection

from test import setup, teardown, random_coord

def test_creatability():
    """ChamplainLabels should exist"""
    lat = random_coord(90)
    lon = random_coord(180)
    
    label = Label(Photograph('demo/IMG_2411.JPG'))
    label.set_location(lat, lon)
    assert isinstance(label, Champlain.Label)
    assert label.get_name() == 'demo/IMG_2411.JPG'
    assert label.get_text() == 'IMG_2411.JPG'
    
    assert label.get_latitude() == lat
    assert label.get_longitude() == lon
    label.photo.destroy()

def test_hoverability():
    """Labels should grow when hovered"""
    assert Photograph.instances
    for photo in Photograph.instances.values():
        assert photo.label.get_scale() == (1, 1)
        photo.label.emit('enter-event', Clutter.Event())
        assert photo.label.get_scale() == (1.05, 1.05)
        photo.label.emit('leave-event', Clutter.Event())
        assert photo.label.get_scale() == (1, 1)

def test_clickability():
    """Labels become selected when clicked"""
    assert Photograph.instances
    for photo in Photograph.instances.values():
        photo.label.emit('button-press', Clutter.Event())
        for button in ('save', 'revert', 'close'):
            assert Widgets[button + '_button'].get_sensitive()
        
        assert selection.iter_is_selected(photo.iter)
        assert selection.count_selected_rows() == 1
        assert photo in selected
        assert len(selected) == 1
        assert photo.label.get_scale() == (1.1, 1.1)
        assert photo.label.get_selected()
        assert photo.label.get_property('opacity') == 255
        
        # Make sure the Labels that we didn't click on are deselected.
        for other in Photograph.instances.values():
            if other.filename == photo.filename:
                continue
            assert not selection.iter_is_selected(other.iter)
            assert other not in selected
            assert other.label.get_scale() == (1, 1)
            assert not other.label.get_selected()
            assert other.label.get_property('opacity') == 64

