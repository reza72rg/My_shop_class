  $(function() {

                $('.form-control').on('click', function() {
                    $('.icp-auto').iconpicker();
                    $('.icp-dd').each(function() {
                        var $this = $(this);
                        $this.iconpicker({
                            title: 'Dropdown with picker',
                            container: $(' ~ .dropdown-menu:first', $this)
						});
					});

				}).trigger('click');

                // Events sample:
                // This event is only triggered when the actual input value is changed
                // by user interaction
                $('.icp').on('iconpickerSelected', function(e) {
                    $('.lead .picker-target').get(0).className = 'picker-target fa-2x ' +
					e.iconpickerInstance.options.iconBaseClass + ' ' +
					e.iconpickerInstance.getValue(e.iconpickerValue);
				});
			});
