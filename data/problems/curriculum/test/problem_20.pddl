

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b10)
(on b2 b1)
(on b3 b9)
(on b4 b6)
(on b5 b8)
(on b6 b3)
(on-table b7)
(on b8 b2)
(on b9 b7)
(on b10 b4)
(clear b5)
)
(:goal
(and
(on b1 b4)
(on b2 b9)
(on b3 b1)
(on b4 b10)
(on b5 b7)
(on b8 b2)
(on b9 b3)
(on b10 b5))
)
)


