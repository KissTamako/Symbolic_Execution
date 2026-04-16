(set-logic ALL)
; Frontier Constraint ID: 57959ce70af02bb9
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2455)) (False)
(assert (not (= x 2455)))

; Query: ((== x 2456)) (False)
(assert (not (not (= x 2456))))

(check-sat)
(get-model)
