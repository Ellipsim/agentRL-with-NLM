

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on-table b1)
(on b2 b1)
(on-table b3)
(on b4 b7)
(on-table b5)
(on b6 b2)
(on b7 b6)
(on-table b8)
(on b9 b8)
(clear b3)
(clear b4)
(clear b5)
(clear b9)
)
(:goal
(and
(on b1 b9)
(on b4 b1)
(on b5 b2)
(on b6 b5)
(on b7 b8))
)
)


