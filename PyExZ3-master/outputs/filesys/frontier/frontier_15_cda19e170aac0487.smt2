(set-logic ALL)
; Frontier Constraint ID: cda19e170aac0487
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1183)) (False)
(assert (not (= x 1183)))

; Query: ((== x 1184)) (False)
(assert (not (not (= x 1184))))

(check-sat)
(get-model)
