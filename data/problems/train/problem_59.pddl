

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b6)
(ontable b3)
(on b4 b3)
(on b5 b9)
(on b6 b8)
(ontable b7)
(on b8 b10)
(on b9 b1)
(on b10 b4)
(clear b2)
(clear b5)
)
(:goal
(and
(on b1 b7)
(on b3 b6)
(on b4 b5)
(on b7 b3)
(on b8 b9)
(on b10 b8))
)
)


