

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b11)
(on b3 b12)
(on b4 b6)
(on b5 b7)
(ontable b6)
(ontable b7)
(on b8 b3)
(on b9 b4)
(ontable b10)
(on b11 b10)
(on b12 b1)
(clear b2)
(clear b5)
(clear b8)
)
(:goal
(and
(on b1 b7)
(on b2 b4)
(on b4 b6)
(on b8 b2)
(on b9 b8)
(on b10 b3)
(on b12 b1))
)
)


