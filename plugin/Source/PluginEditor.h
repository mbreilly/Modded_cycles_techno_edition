#pragma once

#include <juce_audio_processors/juce_audio_processors.h>
#include "PluginProcessor.h"
#include "SampleView.h"
#include <array>
#include <map>

//==============================================================================
class CyclesLookAndFeel : public juce::LookAndFeel_V4
{
public:
    CyclesLookAndFeel();
    void drawRotarySlider (juce::Graphics&, int x, int y, int w, int h, float pos,
                           float startAngle, float endAngle, juce::Slider&) override;
    void drawButtonBackground (juce::Graphics&, juce::Button&, const juce::Colour&,
                               bool highlighted, bool down) override;
    void drawButtonText (juce::Graphics&, juce::TextButton&, bool highlighted, bool down) override;
    void drawComboBox (juce::Graphics&, int width, int height, bool down, int bx, int by, int bw, int bh, juce::ComboBox&) override;
    void positionComboBoxText (juce::ComboBox&, juce::Label&) override;
    juce::Font getComboBoxFont (juce::ComboBox&) override;
    juce::Font getLabelFont (juce::Label&) override;
    void drawLabel (juce::Graphics&, juce::Label&) override;
    juce::PopupMenu::Options getOptionsForComboBoxPopupMenu (juce::ComboBox&, juce::Label&) override;

    /** A level meter (0..1 linear peak). Hardware: green to amber to red; Overbridge and Sleek: segmented, in the
        item's colour, red above -3 dB. */
    static void drawMeter (juce::Graphics&, juce::Rectangle<float>, float peak, bool vertical,
                           juce::Colour item = juce::Colours::transparentBlack);
    /** A section box with its title (MACHINE, FILTER...), drawn the way the look wants it. */
    static void drawSection (juce::Graphics&, const juce::Component&, juce::Rectangle<int> box, const juce::String& title);
    /** Small caps text (letter-spaced in Sleek). */
    static void drawCaps (juce::Graphics&, const juce::String&, juce::Rectangle<int>, float size, juce::Colour,
                          juce::Justification = juce::Justification::centredLeft, bool bold = true);

    // ---- Looks (overbridge-sleek-gui-style): Overbridge (default), Sleek, Hardware (the Steel blue bakelite look)
    enum class Look { overbridge, sleek, hardware };
    static Look look;
    static bool flat()  { return look != Look::hardware; }
    static bool sleek() { return look == Look::sleek; }
    static void applyLook (Look);            // fills the colours below
    void refreshColours();                   // setColour() for the current look (call after applyLook)
    static Look loadSavedLook();             // per user, not per project
    static void saveLook (Look);
    static const char* lookName (Look);

    // Colours of the current look (the Hardware look is "Steel blue", ui-designer/modelcycles-link-colors.html)
    static juce::Colour bg, panel, raised, accent, text, dim, ok, warn, bad, knobTrack, knobBody, outline, comboEdge;

    // Colours by item: tracks 1-6, the FX channel, the mixer. Greys everywhere else.
    enum Item { itemFx = 6, itemMixer = 7, numItems = 8 };
    static juce::Colour items[numItems];
    static void setItem (juce::Component&, int item);
    /** The item colour of the first tagged component from c up (the plain accent on Hardware or when untagged). */
    static juce::Colour accentFor (const juce::Component* c);
    static juce::Colour itemColour (int item) { return flat() && item >= 0 && item < numItems ? items[item] : accent; }
};

//==============================================================================
/** One Model:Cycles parameter: a dial (0-127) or a dropdown, with its name and CC number. */
class ParamControl : public juce::Component, public juce::SettableTooltipClient
{
public:
    ParamControl (juce::AudioProcessorValueTreeState&, const cycles::ParamInfo&, bool compact = false);
    void paint (juce::Graphics&) override;
    void resized() override;

    /** The track's machine changed: relabel (machine knobs and extras take their names from the machine). */
    void machineChanged();

private:
    int machine() const;
    juce::AudioProcessorValueTreeState& apvts;
    const cycles::ParamInfo& info;
    bool compact;
    std::unique_ptr<juce::Slider> slider;
    std::unique_ptr<juce::ComboBox> combo;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> sliderAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::ComboBoxAttachment> comboAttachment;
};

/** A titled grid of ParamControls (one device page). */
class Section : public juce::Component
{
public:
    Section (juce::String title, int columns);
    void add (std::unique_ptr<ParamControl>);
    void machineChanged() { for (auto& c : controls) c->machineChanged(); }
    int  heightFor() const;
    int  widthFor() const { return columns * cellW + 8; }
    void paint (juce::Graphics&) override;
    void resized() override;

    static constexpr int cellW = 94, cellH = 98, titleH = 22;

private:
    juce::String title;
    int columns;
    std::vector<std::unique_ptr<ParamControl>> controls;
};

//==============================================================================
/** Everything for one track (or the FX block), laid out as its pages. */
class TrackView : public juce::Component, private juce::Timer
{
public:
    TrackView (CyclesProcessor&, int slot);
    void paint (juce::Graphics&) override;
    void resized() override;

private:
    void timerCallback() override;
    static constexpr int headerH = 34;
    CyclesProcessor& proc;
    int slot;
    std::map<juce::String, std::unique_ptr<Section>> pages;
    int shownMachine = -1;
    // SAMPLER / GRANULAR / WAVETABLE: the sample window in place of the right column (SAMPLE toggles it)
    std::unique_ptr<SampleView> sampleView;
    juce::TextButton sampleButton { "SAMPLE" };
    bool sampleShown = true;
    void updateSampleView();
    juce::TextButton muteButton { "MUTE" };   // the track's Mute, in the header like Overbridge's track strip
    // FX: a KILL under each master EQ band, like a DJ mixer: the band to 0 (kill), again: back where it was
    std::array<juce::TextButton, 3> killButtons;
    std::array<int, 3> killRestore { 64, 64, 64 };
    void toggleKill (int band);
    std::unique_ptr<juce::ButtonParameterAttachment> muteAttachment;
};

/** Overbridge-style mixer: one strip per track plus the FX return. */
class MixerView : public juce::Component, private juce::Timer
{
public:
    explicit MixerView (CyclesProcessor&);
    void paint (juce::Graphics&) override;
    void resized() override;

private:
    void timerCallback() override { repaint(); }
    CyclesProcessor& proc;
    struct Strip { juce::String title; std::vector<std::unique_ptr<ParamControl>> controls; };
    std::vector<Strip> strips;
};

/** Connection, channels and timing. */
class SetupView : public juce::Component, private juce::Timer
{
public:
    explicit SetupView (CyclesProcessor&);
    void paint (juce::Graphics&) override;
    std::function<void (CyclesLookAndFeel::Look)> onLook; // the Look menu (the editor rebuilds the pages)
    void resized() override;

private:
    void timerCallback() override;
    void refreshPorts();
    void updateEnablement();

    CyclesProcessor& proc;
    juce::Label modeLabel { {}, "Connection" }, inLabel { {}, "MIDI In" }, outLabel { {}, "MIDI Out" },
                offsetLabel { {}, "Clock offset (ms)" }, trimLabel { {}, "Audio trim (ms)" };
    juce::ComboBox modeBox, inBox, outBox;
    juce::TextButton rescan { "Rescan" }, usb2 { "2CH" }, usb6 { "6CH" };
    juce::Label usbLabel { {}, "Device USB audio" }, lookLabel { {}, "Look" };
    juce::ComboBox lookBox;
    juce::Slider offset { juce::Slider::LinearHorizontal, juce::Slider::TextBoxRight },
                 trim { juce::Slider::LinearHorizontal, juce::Slider::TextBoxRight };
    juce::OwnedArray<juce::Label> chanLabels;
    juce::OwnedArray<juce::ComboBox> chanBoxes;
    juce::Array<juce::MidiDeviceInfo> inputs, outputs;
};

//==============================================================================
/** Left-hand rail: track selector with machine name, mute state and MIDI activity. */
class TrackRail : public juce::Component
{
public:
    explicit TrackRail (CyclesProcessor&);
    std::function<void (int)> onSelect; // 0-5 tracks, 6 FX, 7 mixer, 8 setup
    void setSelected (int);
    int  getSelected() const { return selected; }

    void paint (juce::Graphics&) override;
    void mouseDown (const juce::MouseEvent&) override;

    static constexpr int numItems = 9;

private:
    juce::Rectangle<int> itemBounds (int i) const;
    CyclesProcessor& proc;
    int selected = 0;
};

//==============================================================================
/** The project picker under the rail: the device's projects (Modded Cycles firmware with the project list). */
class ProjectBox : public juce::ComboBox
{
public:
    explicit ProjectBox (CyclesProcessor&);
    void refresh();          // items and selection from the processor (message thread)
    void showPopup() override;

private:
    CyclesProcessor& proc;
    int shownSerial = -1;
};

//==============================================================================
class CyclesEditor : public juce::AudioProcessorEditor, private juce::Timer
{
public:
    explicit CyclesEditor (CyclesProcessor&);
    ~CyclesEditor() override;

    void paint (juce::Graphics&) override;
    void resized() override;

    void showView (int index); // see TrackRail::onSelect
    void setLook (CyclesLookAndFeel::Look); // switch the look, save it for this user and rebuild the page

private:
    void timerCallback() override;
    static juce::String describe (juce::uint32 msg);

    CyclesProcessor& proc;
    CyclesLookAndFeel lnf;
    juce::TooltipWindow tooltipWindow { this, 600 };

    juce::TextButton receiveButton { "RECEIVE" }, recallButton { "RECALL" }, clockButton { "CLOCK SYNC" },
                     followButton { "FOLLOW" }, audioButton { "AUDIO" }, sendAllButton { "SEND ALL" },
                     getButton { "GET" };
    TrackRail rail;
    ProjectBox projectBox { proc };
    juce::Rectangle<int> projectArea;
    std::unique_ptr<juce::Component> view;
    int viewIndex = -1, seenSerial = 0, seenGetSerial = 0;
    juce::String flash;
    int flashTicks = 0;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (CyclesEditor)
};
