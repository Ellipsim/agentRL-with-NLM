

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b4)
(on-table b2)
(on b3 b1)
(on b4 b7)
(on-table b5)
(on b6 b9)
(on b7 b5)
(on b8 b3)
(on b9 b2)
(clear b6)
(clear b8)
)
(:goal
(and
(on b4 b7)
(on b5 b4)
(on b6 b9)
(on b9 b1))
)
)


