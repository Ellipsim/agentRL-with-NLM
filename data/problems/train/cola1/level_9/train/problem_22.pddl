

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b3)
(on b3 b9)
(on b4 b8)
(on b5 b6)
(on b6 b4)
(ontable b7)
(on b8 b2)
(ontable b9)
(ontable b10)
(clear b1)
(clear b7)
(clear b10)
)
(:goal
(and
(on b2 b5)
(on b3 b7)
(on b4 b10)
(on b5 b1))
)
)


