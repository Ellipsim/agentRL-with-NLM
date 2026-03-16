

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b7)
(on b3 b9)
(on b4 b1)
(ontable b5)
(on b6 b4)
(on b7 b3)
(on b8 b5)
(ontable b9)
(on b10 b2)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b5)
(on b2 b3)
(on b3 b9)
(on b5 b4)
(on b7 b10)
(on b9 b6))
)
)


