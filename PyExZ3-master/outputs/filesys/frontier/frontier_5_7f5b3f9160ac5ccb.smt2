(set-logic ALL)
; Frontier Constraint ID: 7f5b3f9160ac5ccb
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1318)) (False)
(assert (not (= x 1318)))

; Query: ((== x 1319)) (False)
(assert (not (not (= x 1319))))

(check-sat)
(get-model)
