

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b5)
(on b3 b4)
(on b4 b9)
(on b5 b1)
(on-table b6)
(on b7 b2)
(on b8 b6)
(on b9 b8)
(clear b7)
)
(:goal
(and
(on b2 b3)
(on b3 b9)
(on b7 b8)
(on b8 b5)
(on b9 b1))
)
)


