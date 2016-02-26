#ifndef PHENONDVIHANDLER_HPP
#define PHENONDVIHANDLER_HPP

#include "processorhandler.hpp"

class PhenoNdviHandler : public ProcessorHandler
{
private:
    void HandleJobSubmittedImpl(EventProcessingContext &ctx,
                                const JobSubmittedEvent &event) override;
    void HandleTaskFinishedImpl(EventProcessingContext &ctx,
                                const TaskFinishedEvent &event) override;

    void WriteExecutionInfosFile(const QString &executionInfosPath,
                                 const QStringList &listProducts);

    ProcessorJobDefinitionParams GetProcessingDefinitionImpl(SchedulingContext &ctx, int siteId, int scheduledDate,
                                                const ConfigurationParameterValueMap &requestOverrideCfgValues) override;
};

#endif // PHENONDVIHANDLER_HPP
