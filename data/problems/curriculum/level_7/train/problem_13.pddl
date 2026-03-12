

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b4)
(on b3 b9)
(on-table b4)
(on b5 b7)
(on b6 b5)
(on-table b7)
(on b8 b3)
(on b9 b6)
(clear b1)
(clear b8)
)
(:goal
(and
(on b1 b7)
(on b2 b3)
(on b6 b8)
(on b8 b9)
(on b9 b5))
)
)


