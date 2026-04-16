(set-logic ALL)
; Frontier Constraint ID: 6e209ba6718a0d4e
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1174)) (False)
(assert (not (= x 1174)))

; Query: ((== x 1175)) (False)
(assert (not (not (= x 1175))))

(check-sat)
(get-model)
