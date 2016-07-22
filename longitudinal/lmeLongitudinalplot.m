function [stats] = lmeLongitudinalplot(stats, test_names, subs, time_course);
% [stats] = lmeLongitudinalplot(stats, test_names, subs);
% 
% Function: plots the behavioral data and overlays lme curve
% 
% Inputs:
% stats: in the form of a struct
% 
% Outputs:
% 
% Example:
%

%% Time Variable
if time_course == 1
    x_name = 'hours';
    xx = [0 50 100 150 200];    
elseif time_course == 2
    x_name = 'days'; 
    xx = [0 10 20 30 40 50 60 70]; 
elseif time_course == 3
    x_name = 'session';
    xx = [0 1 2 3 4 5]; 

end

%% Create plots
for ii = 1:length(test_names)
%     subplot(m,n,ii);
    % Create table for individual test
    plot_table = table(stats(ii).data_table.sid, stats(ii).data_table.long_var, ...
         stats(ii).data_table.score);
    % Name variables in plot table
    plot_table.Properties.VariableNames = {'sid', x_name, 'score'};
    % find the number of individual subjects
    s = unique(stats(ii).data_table.sid);
    % Create plot matrix
    plot_matrix = nan(length(plot_table.sid), length(s)); 

    figure; hold;
    % loop over each subject over sessions
    for subj = 1:length(s)
         % find the sessions for each subject
         visit_indx = find(plot_table.sid == s(subj));
         % create empty array for individual subject 
         sub_mat = [];
         % loop over each visit
         for visit = 1:length(visit_indx)
             % assign session values to plot array
             if time_course == 1
                 sub_mat(visit, 1) = plot_table.hours(visit_indx(visit));
                 sub_mat(visit, 2) = plot_table.score(visit_indx(visit));
             elseif time_course == 2
                 sub_mat(visit, 1) = plot_table.days(visit_indx(visit));
                 sub_mat(visit, 2) = plot_table.score(visit_indx(visit));
             elseif time_course == 3
                 sub_mat(visit, 1) = plot_table.session(visit_indx(visit));
                 sub_mat(visit, 2) = plot_table.score(visit_indx(visit));
             end
         end
         % plot the scores, hours v. score
         plot(sub_mat(:,1), sub_mat(:,2),'-o');
    end

    % format the plot nicely
    ylabel(test_names(ii)); xlabel(x_name); 
    legend(subs, 'Location', 'westoutside');
    title([test_names(ii), 'vs ', x_name]);
    grid('on')

    % Add linear line of best fit
    if isnumeric(stats(ii).data_table.long_var)
        low = min(stats(ii).data_table.long_var);
        high = max(stats(ii).data_table.long_var);
        xx = [low low/2 0 high/2 high];
        y = polyval(flipud(stats(ii).lme_linear.Coefficients.Estimate),xx);
        plot(xx,y,'--k','linewidth',2);
        
        %     % Add shaded error bar
        %     err = repmat(stats(ii).lme.Coefficients.SE(2), 1, length(xx));
        %     shadedErrorBar(xx, y, err);
        
        % Add p value for best fit line
        p_linear = double(stats(ii).lme_linear.Coefficients.pValue(2));
        text(-40, 8, num2str(p_linear), 'FontSize', 12);
        
        % Add quadratic line of best fit
        y = polyval(flipud(stats(ii).lme_quad.Coefficients.Estimate),xx);
        plot(xx,y,'--b','linewidth',2);
        
        %      % Add shaded error bar
        %     err = repmat(stats(ii).lme2.Coefficients.SE(3), 1, length(xx));
        %     shadedErrorBar(xx, y, err);
        
        % Add p value for best fit line
        p_quad = double(stats(ii).lme_quad.Coefficients.pValue(3));
        text(-40, 6, num2str(p_quad), 'Color', 'blue', 'FontSize', 12);
        
        % Save image
        test = num2str(cell2mat(test_names(ii)));
        test = strrep(test, '\_', '-');
        fname = sprintf('~/Desktop/figures/LMB/%s-%s.png', test, date);
        print(fname, '-dpng');
        
    end
end



return

