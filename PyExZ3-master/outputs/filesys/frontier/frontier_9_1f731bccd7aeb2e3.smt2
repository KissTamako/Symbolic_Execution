(set-logic ALL)
; Frontier Constraint ID: 1f731bccd7aeb2e3
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1324)) (False)
(assert (not (= x 1324)))

; Query: ((== x 1325)) (False)
(assert (not (not (= x 1325))))

(check-sat)
(get-model)
