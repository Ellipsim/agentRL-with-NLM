

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b8)
(on-table b2)
(on b3 b6)
(on-table b4)
(on b5 b9)
(on b6 b7)
(on b7 b4)
(on b8 b5)
(on b9 b3)
(clear b1)
(clear b2)
)
(:goal
(and
(on b1 b6)
(on b5 b9)
(on b7 b1)
(on b8 b4)
(on b9 b8))
)
)


