

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b8)
(ontable b2)
(on b3 b1)
(ontable b4)
(on b5 b6)
(ontable b6)
(ontable b7)
(on b8 b12)
(on b9 b2)
(on b10 b7)
(ontable b11)
(on b12 b4)
(clear b3)
(clear b5)
(clear b9)
(clear b10)
(clear b11)
)
(:goal
(and
(on b1 b12)
(on b2 b5)
(on b3 b11)
(on b4 b9)
(on b6 b3)
(on b8 b7)
(on b11 b4)
(on b12 b8))
)
)


